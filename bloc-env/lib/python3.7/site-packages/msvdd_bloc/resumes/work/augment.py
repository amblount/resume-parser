import functools as fnc

from msvdd_bloc.resumes import augment_utils as aug


AUGMENTER = aug.Augmenter(
    [
        fnc.partial(aug.delete_token, prob=0.01),
        fnc.partial(aug.insert_whitespace_token, prob=0.01, nrange=(1, 2), field_labels=("field_sep", "item_sep")),
        fnc.partial(aug.change_case_token_text, case="upper", target_labels={"company", "job", "start_dt", "end_dt"}),
        fnc.partial(aug.change_case_token_text, case="lower", target_labels={"start_dt", "end_dt"}),
        fnc.partial(aug.change_case_token_text, case="title", target_labels="highlight"),
    ],
    num=[1.0, 1.0, 0.05, 0.05, 0.025],
)
