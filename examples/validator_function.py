from typing import Annotated, NewType

from pytest import raises

from apischema import ValidationError, deserialize, validator
from apischema.metadata import validators

Palindrome = NewType("Palindrome", str)


@validator  # could also use @validator(owner=Palindrome)
def check_palindrome(s: Palindrome):
    for i in range(len(s) // 2):
        if s[i] != s[-1 - i]:
            raise ValueError("Not a palindrome")


assert deserialize(Palindrome, "tacocat") == "tacocat"
with raises(ValidationError) as err:
    deserialize(Palindrome, "palindrome")
assert err.value.errors == [{"loc": [], "msg": "Not a palindrome"}]

# Using Annotated
with raises(ValidationError) as err:
    deserialize(Annotated[str, validators(check_palindrome)], "palindrom")
assert err.value.errors == [{"loc": [], "msg": "Not a palindrome"}]
