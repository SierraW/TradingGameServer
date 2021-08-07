debug_mode = True
warning_enabled = True


def function_start(function_name: str, args: list[str] = None):
    debug_print('->->->', message=f'Function {function_name} Start', args=args)


def function_end(function_name: str, args: list[str] = None):
    debug_print('<-<-<-', f'Function {function_name} Ended', args=args)


def debug_print(function_name: str, message: str = None, args: list = None):
    if debug_mode:
        if args is None:
            print(f'{function_name} {message}')
        else:
            print(f'{function_name} {message} {args}')


def warning_print(function_name: str, message: str, args: list[str]):
    if warning_enabled:
        print(f'{function_name} {message} args: {args}')