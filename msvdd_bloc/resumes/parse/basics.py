import logging

import probablepeople
import usaddress

from ... import regexes


LOGGER = logging.getLogger(__name__)

LOCATION_TAG_MAPPING = {
   'Recipient': 'recipient',
   'AddressNumber': 'address',
   'AddressNumberPrefix': 'address',
   'AddressNumberSuffix': 'address',
   'StreetName': 'address',
   'StreetNamePreDirectional': 'address',
   'StreetNamePreModifier': 'address',
   'StreetNamePreType': 'address',
   'StreetNamePostDirectional': 'address',
   'StreetNamePostModifier': 'address',
   'StreetNamePostType': 'address',
   'CornerOf': 'address',
   'IntersectionSeparator': 'address',
   'LandmarkName': 'address',
   'USPSBoxGroupID': 'address',
   'USPSBoxGroupType': 'address',
   'USPSBoxID': 'address',
   'USPSBoxType': 'address',
   'BuildingName': 'address',
   'OccupancyType': 'address',
   'OccupancyIdentifier': 'address',
   'SubaddressIdentifier': 'address',
   'SubaddressType': 'address',
   'PlaceName': 'city',
   'StateName': 'region',
   'ZipCode': 'postal_code',
}
"""
Dict[str, str]: Mapping of ``usaddress` location tag to corresponding résumé schema field.
"""


def parse_basics_section(lines):
    """
    Parse a sequence of text lines belonging to the "basics" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeBasicsSchema`.

    Args:
        lines (List[str])

    Returns:
        Dict[str, obj]
    """
    basics = {}
    for line in lines:
        if not line:
            continue
        for line_chunk in regexes.RE_LINE_DELIM.split(line):
            if not line_chunk:
                continue
            if "email" not in basics:
                match = regexes.RE_EMAIL.search(line_chunk)
                if match:
                    basics["email"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "phone" not in basics:
                match = regexes.RE_PHONE_NUMBER.search(line_chunk)
                if match:
                    basics["phone"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "website" not in basics:
                match = regexes.RE_URL.search(line_chunk)
                if match:
                    basics["website"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "profiles" not in basics:
                match = regexes.RE_USER_HANDLE.search(line_chunk)
                if match:
                    basics["profiles"] = [{"username": match.group()}]
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "location" not in basics:
                try:
                    location, location_type = usaddress.tag(
                        line_chunk, tag_mapping=LOCATION_TAG_MAPPING)
                except usaddress.RepeatedLabelError as e:
                    LOGGER.debug("'location' parsing error:\n%s", e)
                    continue
                if location_type == "Street Address":
                    location = dict(location)
                    if "recipient" in location:
                        basics["name"] = location.pop("recipient")
                    basics["location"] = location
            if "name" not in basics:
                try:
                    name, name_type = probablepeople.tag(line_chunk)
                except probablepeople.RepeatedLabelError as e:
                    LOGGER.debug("'name' parsing error:\n%s", e)
                    continue
                if name_type == "Person":
                    basics["name"] = " ".join(name.values())
    return basics
