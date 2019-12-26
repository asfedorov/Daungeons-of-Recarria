import pyglet
import cocos


class MyRectMapLayer(cocos.tiles.RectMapLayer):
    def __init__(self, *args, scale_me=1, **kwargs):
        super().__init__(*args, **kwargs)
        self._scale_me = scale_me

    def set_cell_sprite_opacity(self, i, j, opacity):
        cell = self.get_cell(i, j)
        if cell is None:
            return
        key = cell.origin[:2]
        if key in self._sprites:
            self._sprites[key].opacity = opacity

    def get_visible_cells(self):
        if self.parent.player:
            return {
                self.get_cell(*x)
                for x in self.parent.get_watching_tiles(
                    self.parent.player.position[0],
                    self.parent.player.position[1],
                    watch_range=self.parent.player.watch_range
                )
            }
        x, y = self.view_x / self._scale_me, self.view_y / self._scale_me
        w, h = self.view_w, self.view_h
        return self.get_in_region(x, y, x + w, y + h)

    def get_seen_cells(self):
        x, y = self.view_x / self._scale_me, self.view_y / self._scale_me
        w, h = self.view_w, self.view_h
        return {
            self.get_cell(*x)
            for x in self.parent.seen
        } & set(self.get_in_region(x, y, x + w, y + h))

    def get_longseen_cells(self):
        x, y = self.view_x / self._scale_me, self.view_y / self._scale_me
        w, h = self.view_w, self.view_h
        return {
            self.get_cell(*x)
            for x in set(self.parent.longseen) - set(self.parent.seen)
        } & set(self.get_in_region(x, y, x + w, y + h))

    def get_key_at_pixel(self, x, y):
        """returns the grid coordinates for the hex that covers the point (x, y)"""
        return (int((x - self.origin_x) // self.tw / self._scale_me),
                int((y - self.origin_y) // self.th / self._scale_me))

    def _update_sprite_set(self):
        # update the sprites set
        keep = set()
        visible = self.get_visible_cells()
        for cell in visible:
            if not cell:
                continue
            cx, cy = key = cell.origin[:2]
            keep.add(key)
            if cell.tile is None:
                continue
            if key in self._sprites:
                s = self._sprites[key]
            else:
                s = pyglet.sprite.Sprite(cell.tile.image,
                                         x=cx, y=cy, batch=self.batch)
                if 'color4' in cell.properties:
                    r, g, b, a = cell.properties['color4']
                    s.color = (r, g, b)
                    s.opacity = a
                self._sprites[key] = s

            s.opacity = 255

        for cell in self.get_seen_cells() - set(visible):
            if not cell:
                continue

            cx, cy = key = cell.origin[:2]
            keep.add(key)
            if cell.tile is None:
                continue
            if key in self._sprites:
                s = self._sprites[key]
            else:
                s = pyglet.sprite.Sprite(cell.tile.image,
                                         x=cx, y=cy, batch=self.batch)
                if 'color4' in cell.properties:
                    r, g, b, a = cell.properties['color4']
                    s.color = (r, g, b)
                    s.opacity = a
                self._sprites[key] = s

            s.opacity = 40

        for cell in self.get_longseen_cells() - set(visible):
            if not cell:
                continue

            cx, cy = key = cell.origin[:2]
            keep.add(key)
            if cell.tile is None:
                continue
            if key in self._sprites:
                s = self._sprites[key]
            else:
                s = pyglet.sprite.Sprite(cell.tile.image,
                                         x=cx, y=cy, batch=self.batch)
                if 'color4' in cell.properties:
                    r, g, b, a = cell.properties['color4']
                    s.color = (r, g, b)
                    s.opacity = a
                self._sprites[key] = s

            s.opacity = 25

        for k in list(self._sprites):
            if k not in keep and k in self._sprites:
                self._sprites[k]._label = None
                del self._sprites[k]


class MyRectCell(cocos.tiles.RectCell):
    def __init__(self, *args, view_block=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_block = view_block
