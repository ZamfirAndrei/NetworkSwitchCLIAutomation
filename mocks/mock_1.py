


paths_dut1 = {

    "tftp": "/AGZamfir/Andrei-2028.conf",
    "sftp": "/AGZamfir/sftp_Andrei-2028.conf"
}

paths_dut2 = {

    "tftp": "/AGZamfir/Andrei-2010.conf",
    "sftp": "/AGZamfir/sftp_Andrei-2010.conf"
}

paths_dut3 = {

    "tftp": "/AGZamfir/Andrei-3052.conf",
    "sftp": "/AGZamfir/sftp_Andrei-3052.conf"
}

paths_dut4 = {

    "tftp": "/AGZamfir/new1.conf",
    "sftp": "/AGZamfir/sftp_new1.conf"
}

paths_dut5 = {

    "tftp": "/AGZamfir/cip52.conf",
    "sftp": "/AGZamfir/sftp_cip52.conf"
}

paths_dut6 = {

    "tftp": "/AGZamfir/3024F.conf",
    "sftp": "/AGZamfir/sftp_3024F.conf"
}

paths = {

    "DUT1": paths_dut1,
    "DUT2": paths_dut2,
    "DUT3": paths_dut3,
    "DUT4": paths_dut4,
    "DUT5": paths_dut5,
    "DUT6": paths_dut6,
}

images_fiber = {

    "image_to_upgrade" : "6.0-101",
    "image_to_downgrade" : "6.0-r2",
    "image_18" : "6.0-101",
    "image_17" : "6.1.0-e445",
    "image_16" : "6.1.0-e434",
    "image_15" : "6.0.1-r1",
    "image_14" : "6.0-r2",
    "image_13" : "6.0-b9",
    "image_12" : "6.0.0-e91",
    "image_11" : "6.0.0-e75",
    "image_10" : "6.0.0-e74",
    "image_9" : "6.0.0-e73",
    "image_8" : "6.0-b7",
    "image_7" : "6.0-b6",
    "image_6" : "6.0-b4",
    "image_5" : "6.0-b3",
    "image_4" : "6.0.0-e63",
    "image_3" : "6.0.0-e57",
    "image_2" : "6.0.0-e44",
    "image_1" : "6.0.0-e38",
}

images_legacy_EXTX = {

    "image_to_upgrade": "5.0.3-r4",
    "image_to_downgrade": "5.0.3-r3",
    "image_10" : "6.1.0-e451",
    "image_9" : "5.0.3-r3",
    "image_8" : "6.1.0-e445",
    "image_7" : "6.1.0-e434",
    "image_6" : "5.0.2-r4",
    "image_5" : "5.0.1-r4",
    "image_4" : "5.0.1-r3",
    "image_3" : "5.0-r4",
    "image_2" : "4.6-r2",
    "image_1" : "4.4-r3",
}

modes = {

    "tftp" : "tftp",
    "sftp" : "sftp"
}

protocols = {

    "telnet" : "telnet",
    "ssh" : "ssh",
    "scp" : "scp"
}

mocks_sanity_legacy = {

    "server_ip" : "10.2.109.24",
    "protocol" : protocols,
    "user" : "cambium",
    "password" : "cambium123",
    "mode": modes,
    "image_version": images_legacy_EXTX,
    "path": paths,
    "image_version_to_be_checked": images_legacy_EXTX,
    "platform": "EXTX",
    "image_compression" : "img"

}

mocks_sanity_fiber = {

    "server_ip" : "10.2.109.24",
    "protocol" : protocols,
    "user" : "cambium",
    "password" : "cambium123",
    "mode": modes,
    "image_version": images_fiber,
    "path": paths,
    "image_version_to_be_checked": images_fiber,
    "platform": "EX3Kext",
    "image_compression" : "itb"

}
