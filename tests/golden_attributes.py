import os
import pdsviewable

def get_attribute_as_string(obj, attr_name):
    try:
        value = getattr(obj, attr_name)
    except Exception as e:
        return 'EXCEPTION: %r' % (e,)
    
    # repr() for PdsViewSet returns a string with the memory
    # location embedded it in, so we can't compare two values.
    # Instead, we'll convert it into a list of absolute paths of
    # its contents.
    if isinstance(value, pdsviewable.PdsViewSet):
        value = sorted({viewable.abspath for viewable in value.viewables})
    return repr(value)

ATTRIBUTES = {
    '_iconset',
    '_info',
    '_volume_info',
    'absolute_or_logical_path',
    'alt',
    'anchor',
    'checksum',
    'childnames',
    'continuous_view_allowed',
    # 'data_abspaths',
    'date',
    'description',
    'exact_archive_url',
    'exact_checksum_url',
    'exists',
    'extension',
    'filename_keylen',
    'filespec',
    'formatted_size',
    'global_anchor',
    'grid_view_allowed',
    'has_neighbor_rule',
    'height',
    'html_path',
    'icon_type',
    'iconset_closed',
    'iconset_open',
    'info_basename',
    'internal_link_info',
    'is_index',
    'is_viewable',
    'isdir',
    'islabel',
    'label_abspath',
    'label_basename',
    'linked_abspaths',
    'local_viewset',
    'mime_type',
    'modtime',
    'multipage_view_allowed',
    'opus_format',
    'opus_id',
    'opus_type',
    'parent_logical_path',
    'size_bytes',
    'split',
    'url',
    'version_ranks',
    'viewset',
    'volume_data_set_ids',
    'volume_publication_date',
    'volume_version_id',
    'width'
    }    
