from collections import Iterable
import xml.etree.ElementTree as ET

from ngenix_test.serializer.base import BaseSerializer


class XMLSerializer(BaseSerializer):
    name = 'xml'

    def serialize(self, obj):
        if len(obj.__slots__) > 1:
            return self._serialize_tag_extend(obj)
        return self._serialize_tag(obj)

    def deserialize(self, s):
        # FIXME: hardcoded object map
        from ngenix_test.models import Root, Object
        tag_map = {
            'root': Root,
            'object': Object
        }

        return self._deserialize_tag_extended(ET.fromstring(s), tag_map)

    @staticmethod
    def _deserialize_tag(tag, tag_map):
        tag_class = tag_map.get(tag.tag, None)

        if tag_class is None:
            return None

        tag_object = tag_class()
        for attrib in tag.attrib:
            setattr(tag_object, attrib, tag.attrib.get(attrib))
        return tag_object

    def _deserialize_tag_extended(self, tag, tag_map):
        tag_object = self._deserialize_tag(tag, tag_map)

        for tag_child in tag:
            if tag_child.tag == 'var':
                setattr(tag_object, tag_child.attrib.get('name'), tag_child.attrib.get('value'))
            else:
                setattr(tag_object, tag_child.tag, [self._deserialize_tag(t, tag_map) for t in tag_child])
        return tag_object

    @staticmethod
    def _serialize_tag(obj):
        s = "<{}".format(obj.__class__.__name__.lower())
        for name in obj.__slots__:
            s += ' '
            value = getattr(obj, name, None)
            s += "{name}=\"{value}\"".format(name=name, value=value)
        s += ' />'
        return s

    def _serialize_tag_extend(self, obj):
        tag_name = obj.__class__.__name__.lower()
        s = "<{}>".format(tag_name)

        for name in obj.__slots__:
            s += '\n'
            value = getattr(obj, name, None)

            if not isinstance(value, str) and isinstance(value, Iterable):
                s += """<{0}>\n{1}\n</{0}>""".format(
                    name.lower(), '\n'.join(self.serialize(t) for t in value)
                )
            else:
                s += "<var name=\"{name}\" value=\"{value}\" />".format(name=name, value=value)
        s += "\n</{}>".format(tag_name)
        return s
