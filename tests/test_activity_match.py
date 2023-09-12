from tasks.to_be_moved.scripts.check_overlap import check_parcel_overlap


def test_activity_parcel_overlaps_itself():
    check_parcel_overlap(activity_geometry, grist_geometry)