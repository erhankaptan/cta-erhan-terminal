# ============================================================


from __future__ import annotations


from .master_source_universe import (
    HIGH_VALUE_HUMANS_25,
    INSTITUTIONAL_CTAS,
    MASTER_SOURCES,
    MASTER_X_HANDLES,
)


EXPECTED_MASTER_IDS = {
    "master.x.rjparkerjr09",
    "master.x.rjpjr12",
    "master.tick_bill",
    "master.institution.crabel",
    "master.institution.dynamic_beta",
    "master.institution.qim",
    "master.institution.qbasis",
    "master.institution.typhon_capital",
}


def validate_master_x() -> None:
    handles = tuple(MASTER_X_HANDLES)


    assert len(handles) == 69
    assert len(set(handles)) == 69


    assert "@rjparkerjr09" in handles
    assert "@rjpjr12" in handles
    assert "@rjparkerjr12" not in handles


def validate_high_value_human_view() -> None:
    master_x = set(MASTER_X_HANDLES)
    high_value = set(HIGH_VALUE_HUMANS_25)


    assert len(HIGH_VALUE_HUMANS_25) == 25


    intersection = master_x & high_value
    outside = high_value - master_x


    assert len(intersection) == 24
    assert outside == {"@TheStalwart"}


def validate_institutional_cta() -> None:
    assert len(INSTITUTIONAL_CTAS) == 5


def validate_tick_bill() -> None:
    matches = [
        source
        for source in MASTER_SOURCES
        if source.master_source_id == "master.tick_bill"
    ]


    assert len(matches) == 1


    tick_bill = matches[0]


    assert tick_bill.access_channels == ()
    assert tick_bill.source_identity_status.name == "UNRESOLVED"


def validate_master_source_ids() -> None:
    actual_ids = {
        source.master_source_id
        for source in MASTER_SOURCES
    }


    assert EXPECTED_MASTER_IDS.issubset(actual_ids)


    assert "src_x_rjparkerjr09" not in actual_ids
    assert "src_x_rjpjr12" not in actual_ids
    assert "src_special_tick_bill" not in actual_ids


def validate_no_automatic_verified() -> None:
    for source in MASTER_SOURCES:
        assert source.source_identity_status.name == "UNRESOLVED"


def validate_institutional_channels() -> None:
    institutional_ids = {
        source_id
        for source_id, _, _ in INSTITUTIONAL_CTAS
    }


    for source in MASTER_SOURCES:
        if source.master_source_id in institutional_ids:
            assert source.access_channels == ()


def validate_persistence() -> None:
    actual_ids = {
        source.master_source_id
        for source in MASTER_SOURCES
    }


    assert "master.x.rjparkerjr09" in actual_ids
    assert "master.x.rjpjr12" in actual_ids
    assert "master.tick_bill" in actual_ids


def run_integrity_validation() -> None:
    validate_master_x()
    validate_high_value_human_view()
    validate_institutional_cta()
    validate_tick_bill()
    validate_master_source_ids()
    validate_no_automatic_verified()
    validate_institutional_channels()
    validate_persistence()


# ============================================================
