from Notion.Property import Property
from Notion.NotionObject import NotionObject

class Page(NotionObject):
    def get_properties(self) -> list[Property]:
        results = []

        id_dict = self.data['properties']

        for pname in id_dict:
            p = self._get_property(id_dict[pname]['id'])

            ptype = p['type']
            results.append(Property(pname, ptype, p[ptype]))

        return results

    def get_title(self) -> str:
        return self._get_property('title')['title']['plain_text']

    def _get_property(self, propertyID: str):
        p = self._client.get_property(self.get_page_id(), propertyID)

        try:
            if p['object'] == 'list':
                p = p['results'][0]
        except IndexError:
            print(f"=== Failed to get property {propertyID} ===")

        return p

    def get_page_id(self) -> str:
        return self.data['id']

    def update(self, properties: list[Property]):
        self._client.update_page(self.get_page_id(), properties)