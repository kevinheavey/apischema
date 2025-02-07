from dataclasses import InitVar, dataclass, field

from pytest import raises

from apischema import ValidationError, deserialize, validator
from apischema.metadata import init_var


@dataclass
class Foo:
    bar: InitVar[int] = field(metadata=init_var(int))

    @validator(bar)
    def validate(self, bar: int):
        if bar < 0:
            yield "negative"


with raises(ValidationError) as err:
    deserialize(Foo, {"bar": -1})
assert err.value.errors == [{"loc": ["bar"], "msg": "negative"}]
