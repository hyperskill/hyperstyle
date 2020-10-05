def calculate(action: str, operand1: int, operand2: int) -> int:
    if action == '+':
        return operand1 + operand2
    elif action == '-':
        return operand1 - operand2
    elif action == '*':
        return operand1 * operand2
    else:
        raise ValueError(f'Unknown action {action}')
