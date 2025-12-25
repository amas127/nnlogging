import datetime
import uuid

import dateutil
import duckdb
import numpy as np
import pytest

from nnlogging.helpers import dumps, loads


@pytest.fixture
def con():
    con = duckdb.connect()
    con.execute("CREATE TABLE IF NOT EXISTS tb (js JSON)")
    return con


def insert_value_and_get(con, o):
    con.execute("INSERT INTO tb (js) VALUES (?)", (o,))
    tb = con.execute("SELECT js FROM tb").fetchone()
    assert tb is not None and len(tb) == 1
    return tb[0]


class TestJsonTable:
    """Tests for JSON table creation and basic operations"""

    def test_create_json_table(self, con):
        con.execute("DESCRIBE tb")

    def test_insert_select(self, con):
        insert_value_and_get(con, dumps({"m1": "v1"}))
        insert_value_and_get(con, dumps({"m2": "v2"}))
        js1 = con.execute(
            "SELECT js->'m1' FROM tb WHERE js->>'m1' IS NOT NULL"
        ).fetchall()
        assert len(js1) == 1 and len(js1[0]) == 1
        assert js1[0][0] != "v1"
        assert loads(js1[0][0]) == "v1"
        js2 = con.execute(
            "SELECT js->>'m2' FROM tb WHERE js->>'m2' IS NOT NULL"
        ).fetchall()
        assert len(js2) == 1 and len(js2[0]) == 1
        assert js2[0][0] == "v2"


class TestJsonTypeHandling:
    @pytest.mark.parametrize(
        "obj",
        [
            1,
            1.0,
            True,
            "str",
            datetime.datetime.now(),
            uuid.uuid4(),
            np.random.normal(size=(2, 2)),
            None,
        ],
    )
    def test_insert_plain_as_jsonlike(self, obj, con):
        js = insert_value_and_get(con, dumps(obj))
        match obj:
            case datetime.datetime():
                assert dateutil.parser.parse(loads(js)) == obj
            case uuid.UUID():
                assert uuid.UUID(loads(js)) == obj
            case np.ndarray():
                assert (np.array(loads(js)) == obj).all()
            case _:
                assert loads(js) == obj

    def test_insert_set_as_jsonlike(self, con):
        obj = {"1", "2"}
        with pytest.raises(TypeError):
            _ = insert_value_and_get(con, dumps(obj))

    def test_insert_tuple_as_jsonlike(self, con):
        obj = ("1", "2")
        js = insert_value_and_get(con, dumps(obj))
        assert js == '["1","2"]'
        assert loads(js) == list(obj)
