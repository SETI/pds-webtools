import pdsfile
import translator
import re

opus_id_list = [
    'vg-pps-2-n-occ-1989-236-sigsgr-i',
    'vg-pps-2-s-occ-1981-238-delsco-e',
    'vg-pps-2-u-occ-1986-024-alpha-betper-e',
    'vg-pps-2-u-occ-1986-024-alpha-betper-i',
    'vg-pps-2-u-occ-1986-024-beta-betper-e',
    'vg-pps-2-u-occ-1986-024-beta-betper-i',
    'vg-pps-2-u-occ-1986-024-delta-betper-e',
    'vg-pps-2-u-occ-1986-024-delta-betper-i',
    'vg-pps-2-u-occ-1986-024-delta-sigsgr-e',
    'vg-pps-2-u-occ-1986-024-delta-sigsgr-i',
    'vg-pps-2-u-occ-1986-024-epsilon-betper-e',
    'vg-pps-2-u-occ-1986-024-epsilon-betper-i',
    'vg-pps-2-u-occ-1986-024-epsilon-sigsgr-e',
    'vg-pps-2-u-occ-1986-024-epsilon-sigsgr-i',
    'vg-pps-2-u-occ-1986-024-eta-betper-e',
    'vg-pps-2-u-occ-1986-024-eta-betper-i',
    'vg-pps-2-u-occ-1986-024-five-betper-e',
    'vg-pps-2-u-occ-1986-024-five-betper-i',
    'vg-pps-2-u-occ-1986-024-four-betper-e',
    'vg-pps-2-u-occ-1986-024-four-betper-i',
    'vg-pps-2-u-occ-1986-024-gamma-betper-e',
    'vg-pps-2-u-occ-1986-024-gamma-betper-i',
    'vg-pps-2-u-occ-1986-024-lambda-sigsgr-e',
    'vg-pps-2-u-occ-1986-024-lambda-sigsgr-i',
    'vg-pps-2-u-occ-1986-024-ringpl-betper-e',
    'vg-pps-2-u-occ-1986-024-ringpl-betper-i',
    'vg-pps-2-u-occ-1986-024-ringpl-sigsgr-e',
    'vg-pps-2-u-occ-1986-024-ringpl-sigsgr-i',
    'vg-pps-2-u-occ-1986-024-six-betper-e',
    'vg-pps-2-u-occ-1986-024-six-betper-i',
    'vg-rss-1-s-occ-1980-318-s63-e',
    'vg-rss-1-s-occ-1980-318-x63-e',
    'vg-rss-2-u-occ-1986-024-alpha-s43-e',
    'vg-rss-2-u-occ-1986-024-alpha-s43-i',
    'vg-rss-2-u-occ-1986-024-alpha-x43-e',
    'vg-rss-2-u-occ-1986-024-alpha-x43-i',
    'vg-rss-2-u-occ-1986-024-beta-s43-e',
    'vg-rss-2-u-occ-1986-024-beta-s43-i',
    'vg-rss-2-u-occ-1986-024-beta-x43-e',
    'vg-rss-2-u-occ-1986-024-beta-x43-i',
    'vg-rss-2-u-occ-1986-024-delta-s43-e',
    'vg-rss-2-u-occ-1986-024-delta-s43-i',
    'vg-rss-2-u-occ-1986-024-delta-x43-e',
    'vg-rss-2-u-occ-1986-024-delta-x43-i',
    'vg-rss-2-u-occ-1986-024-epsilon-s43-e',
    'vg-rss-2-u-occ-1986-024-epsilon-s43-i',
    'vg-rss-2-u-occ-1986-024-epsilon-x43-e',
    'vg-rss-2-u-occ-1986-024-epsilon-x43-i',
    'vg-rss-2-u-occ-1986-024-eta-s43-e',
    'vg-rss-2-u-occ-1986-024-eta-s43-i',
    'vg-rss-2-u-occ-1986-024-eta-x43-e',
    'vg-rss-2-u-occ-1986-024-eta-x43-i',
    'vg-rss-2-u-occ-1986-024-five-s43-e',
    'vg-rss-2-u-occ-1986-024-five-s43-i',
    'vg-rss-2-u-occ-1986-024-five-x43-e',
    'vg-rss-2-u-occ-1986-024-five-x43-i',
    'vg-rss-2-u-occ-1986-024-four-s43-e',
    'vg-rss-2-u-occ-1986-024-four-s43-i',
    'vg-rss-2-u-occ-1986-024-four-x43-e',
    'vg-rss-2-u-occ-1986-024-four-x43-i',
    'vg-rss-2-u-occ-1986-024-gamma-s43-e',
    'vg-rss-2-u-occ-1986-024-gamma-s43-i',
    'vg-rss-2-u-occ-1986-024-gamma-x43-e',
    'vg-rss-2-u-occ-1986-024-gamma-x43-i',
    'vg-rss-2-u-occ-1986-024-six-s43-e',
    'vg-rss-2-u-occ-1986-024-six-s43-i',
    'vg-rss-2-u-occ-1986-024-six-x43-e',
    'vg-rss-2-u-occ-1986-024-six-x43-i',
    'vg-uvs-1-s-occ-1980-317-iother-e',
    'vg-uvs-2-n-occ-1989-236-sigsgr-i',
    'vg-uvs-2-s-occ-1981-237-delsco-i',
    'vg-uvs-2-s-occ-1981-238-delsco-e',
    'vg-uvs-2-u-occ-1986-024-sigsgr-delta-e',
    'vg-uvs-2-u-occ-1986-024-sigsgr-delta-i',
    'vg-uvs-2-u-occ-1986-024-sigsgr-epsilon-e',
    'vg-uvs-2-u-occ-1986-024-sigsgr-epsilon-i',
    'vg-uvs-2-u-occ-1986-024-sigsgr-ringpl-e',
    'vg-uvs-2-u-occ-1986-024-sigsgr-ringpl-i'
]
list_dir = f"./files_with_missing_cat.txt"
# Write proposal ids into proposal_ids.txt
with open(list_dir, "w") as f:
    for id in opus_id_list:
        try:
            pdsf = pdsfile.PdsFile.from_opus_id(id);
        except ValueError:
            f.write("%s\n" % '============================')
            f.write("%s\n" % 'Unrecognized opus id:')
            f.write("%s\n" % id)
            continue
        # print('============================')
        # print(pdsf.logical_path)
        # print(files)
        opus_products_cat = pdsf.opus_products().keys()
        if '' in opus_products_cat:
            files = pdsf.opus_products()['']
            f.write("%s\n" % '============================')
            f.write("%s\n" % 'Test case:')
            f.write("%s\n" % pdsf.logical_path)
            f.write("%s\n" % 'OPUS ID:')
            f.write("%s\n" % id)
            f.write("%s\n" % 'Files without opus_type in opus_products return:')
            # f.write("%s\n" % files)
            for file_li in files:
                for file in file_li:
                    f.write("%s\n" % file.logical_path)
