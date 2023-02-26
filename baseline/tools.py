import copy
import typing

import erutils

from modules.models import CGRModel

VERSIONS: typing.Optional[list[str]] = [
    'v2', 'v3', 'v4'
]
BLACK_WORDS_LIST: typing.Optional[list[str]] = [
    'matin'
]

ALLOWED_SAVE_FORMATS: typing.Optional[list[str]] = [
    'png', 'jpg'
]

TASKS: typing.Optional[list[str]] = [
    'PIL', 'dict', 'cv', 'np', 'save', 'check'
]


def using_v4(prompt: typing.Optional[str]) -> typing.Optional[str]:
    prompt += ', mdjrny-v4 style'
    return prompt


def using_v3(prompt: typing.Optional[str]) -> typing.Optional[str]:
    prompt += ', mdjrny-v3 style'
    return prompt


def using_v2(prompt: typing.Optional[str]) -> typing.Optional[str]:
    prompt += ', mdjrny-v2 style'
    return prompt


def using_realistic(prompt: typing.Optional[str]) -> typing.Optional[str]:
    prompt += ', realistic style'
    return prompt


def run_save(prompt: typing.Union[str, list[str]], model: typing.Optional[CGRModel]) -> None:
    predictions = model(prompt).images[0]
    erutils.fprint(f'Writing Predictions To PNG format as an image into file [{prompt}.png]')
    predictions.save(f'{prompt}.png')
    return None


def check_prompt(prompt: typing.Optional[str]) -> typing.Union[str, None]:
    """

    :param prompt: prompt to be checked if some words are not available in that
    :return: prompt or None
    """
    _s = prompt.split()
    if _s not in BLACK_WORDS_LIST:
        return prompt
    else:
        erutils.fprint('BLACK WORDS DETECTED', erutils.Cp.RED)
        return None


def v_to_prompt(prompt: typing.Union[str, typing.List[str]]):
    if use_check_prompt:
        prompt = check_prompt(prompt)
    if prompt is not None:
        if version in VERSIONS:

            if use_version:
                if version == VERSIONS[0]:
                    prompt = using_v2(prompt)
                elif version == VERSIONS[1]:
                    prompt = using_v3(prompt)
                elif version == VERSIONS[2]:
                    prompt = using_v4(prompt)
        if use_realistic:
            prompt = using_realistic(prompt)
    return prompt


def generate(prompt: typing.Union[str, list[str]], model: typing.Optional[CGRModel],
             size: typing.Optional[typing.Tuple] = None,
             use_version: typing.Optional[bool] = True, version: typing.Optional[str] = 'v4',
             use_realistic: typing.Optional[bool] = False, image_format: typing.Optional[str] = 'png',
             use_check_prompt:
             typing.Optional[bool] = False, task: typing.Optional[str] = 'save'):
    if task == 'save' and image_format not in ALLOWED_SAVE_FORMATS:
        raise ValueError(
            f'stop execution of command cause provided format not available in formats : \n '
            f'[provided : {image_format}  |  formats :{ALLOWED_SAVE_FORMATS}]'
        )
    if image_format not in ALLOWED_SAVE_FORMATS:
        raise Warning(f'provided format not available in formats : \n '
                      f'[provided : {image_format}  |  formats :{ALLOWED_SAVE_FORMATS}]')
    if use_version and version is None:
        raise ValueError(
            f'use_version has been set to True but not version provided [use_version : {use_version} |'
            f' version : {version}]')
    elif use_version and use_realistic:
        raise ValueError(
            f'you only can use custom versions or realistic s you can"t use both of them'
            f'at last at this version'
        )
    else:
        ...
    if task not in TASKS:
        raise ValueError(f'specified task should be in list of tasks \n {TASKS}')
    org_p = copy.deepcopy(prompt)

    size = (None, None) if size is None else size
    if isinstance(prompt, str):
        prompt = v_to_prompt(prompt)
    elif isinstance(prompt, list):
        prompt = [v_to_prompt(p) for p in prompt]
    else:
        raise ValueError('Wrong input for prompt input should be string or a list of strings')
    print(f'PROMPT :  {prompt} | SIZE : {size}')

    generated_sample = model(prompt=prompt, height=size[0], width=size[1])
    if task == 'PIL':
        return generated_sample.images[0]
    elif task == 'dict':
        return dict(
            image=generated_sample.images[0],
            content=generated_sample,
            size=None,
            nsfw=False,
        )
    elif task == 'cv':
        return NotImplementedError
    elif task == 'np':
        return NotImplementedError
    elif task == 'check':
        return True
    elif task == 'save':
        try:
            generated_sample.images[0].save(f'{org_p}.{image_format}')
            return True
        except Warning as w:
            return False
    else:
        raise ValueError('selected task is going to be available in future')