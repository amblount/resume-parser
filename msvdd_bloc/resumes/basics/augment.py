import functools as fnc

from msvdd_bloc.resumes import augment_utils as aug


AUGMENTER = aug.Augmenter(
    [
        fnc.partial(aug.delete_token, prob=0.01),
        fnc.partial(aug.change_case_token_text, case="title", target_labels={"label",}),
        fnc.partial(aug.change_case_token_text, case="upper", target_labels={"name",}),
        fnc.partial(aug.change_case_token_text, case="title", target_labels={"website_profile",}),
    ],
    num=[1.0, 0.25, 0.05, 0.01],
)
