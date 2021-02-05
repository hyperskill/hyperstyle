def get_bool_expr_len_tip() -> str:
    return 'Too long boolean expression. ' \
           'Try to split it into smaller expressions.'


def get_func_len_tip() -> str:
    return 'Too long function. ' \
           'Try to split it into smaller functions / methods.' \
           'It will make your code easy to understand and less error prone.'


def get_line_len_tip() -> str:
    return 'Too long line. ' \
           'Try to split it into smaller lines.' \
           'It will make your code easy to understand.'


def get_cyclomatic_complexity_tip() -> str:
    return 'Too complex function. You can figure out how to simplify this code ' \
           'or split it into a set of small functions / methods. ' \
           'It will make your code easy to understand and less error prone.'


def add_complexity_tip(description: str) -> str:
    description = description.strip()
    description = description[:-1] if description.endswith('.') else description
    description = description.replace('NCSS', 'Non Commenting Source Statements metric')
    return description + ('. You can figure out how to simplify this code '
                          'or split it into a set of small functions / methods. '
                          'It will make your code easy to understand and less error prone.')


def get_inheritance_depth_tip() -> str:
    return 'Too deep inheritance tree is complicated to understand. ' \
           'Try to reduce it (maybe you should use a composition instead).'


# This issue will not be reported at this version
def get_child_number_tip() -> str:
    return ''


def get_weighted_method_tip() -> str:
    return 'The number of methods and their complexity may be too hight. ' \
           'It may require too much time and effort to develop and maintain the class.'


def get_class_coupling_tip() -> str:
    return 'The class seems to depend on too many other classes. ' \
           'Increased coupling increases interclass dependencies, ' \
           'making the code less modular and less suitable for reuse and testing.'


# This issue will not be reported at this version
def get_cohesion_tip() -> str:
    return ''


def get_class_response_tip() -> str:
    return 'The class have too many methods that can potentially ' \
           'be executed in response to a single message received by an object of that class. ' \
           'The larger the number of methods that can be invoked from a class, ' \
           'the greater the complexity of the class'


def get_method_number_tip() -> str:
    return 'The file has too many methods inside and is complicated to understand. ' \
           'Consider its decomposition to smaller classes.'
