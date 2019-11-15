FIELD_LABEL_SEPS = (":", "-")
FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�", "⇧")
ITEM_SEPS = (",", ";")

FIELD_LABEL_ADDRS = ("Address", "Current Address")
FIELD_LABEL_EMAILS = ("Email", "E-mail")
FIELD_LABEL_PHONES = ("Phone", "Mobile", "Cell", "Tel.")
FIELD_LABEL_PROFILES = ("GitHub", "Twitter", "LinkedIn", "Portfolio")

PHONE_FORMATS = (
    "###-###-####", "###.###.####", "(###) ###-####", "### ###-####",
)
URL_SCHEMES = ("www.", "http://", "http://www.")

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
