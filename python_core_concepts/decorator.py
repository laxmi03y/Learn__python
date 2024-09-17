def convert_strings_to_integers(func):
    def wrapper(a, b):
        print(a, b)
        try:
            a,b= int(a),int(b)
        except Exception as e:
            print(e)
        return func(a, b)

    return wrapper

@convert_strings_to_integers
def sum_func(a, b):
    return a + b


sum_result = sum_func(10, "20")

print("result-->", sum_result)