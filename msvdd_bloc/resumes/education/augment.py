import functools as fnc

from msvdd_bloc.resumes import noise_utils


NOISER = noise_utils.BaseNoiser(
    [
        fnc.partial(noise_utils.delete_token, prob=0.01),
        fnc.partial(noise_utils.change_case_token_text, case="upper", target_labels={"institution",}),
        fnc.partial(noise_utils.change_case_token_text, case="upper", target_labels={"end_dt", "start_dt"}),
    ],
    num=[1.0, 0.05, 0.025],
)
