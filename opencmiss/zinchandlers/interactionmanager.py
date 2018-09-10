

class InteractionManager(object):

    def __init__(self):
        self._handlers = {}
        self._key_code_handler_map = {}
        self._active_handler = None
        self._fallback_handler = None

    def register_handler(self, handler):
        handler.set_zinc_sceneviewer(self._sceneviewer)
        self._handlers[handler.get_mode()] = handler

        if hasattr(handler, 'get_key_code'):
            key_code = handler.get_key_code()
            self._key_code_handler_map[key_code] = handler

        if self._fallback_handler is None:
            self._fallback_handler = handler
            self._active_handler = handler

    def set_fallback_handler(self, fallback_handler):
        self._fallback_handler = fallback_handler

    def key_press_event(self, event):
        if event.key() in self._key_code_handler_map and not event.isAutoRepeat():
            event.accept()
            self._active_handler.leave()
            self._active_handler = self._key_code_handler_map[event.key()]
            self._active_handler.enter()
        else:
            event.ignore()

    def key_release_event(self, event):
        if event.key() in self._key_code_handler_map and not event.isAutoRepeat():
            event.accept()
            self._active_handler.leave()
            self._active_handler = self._fallback_handler
            self._active_handler.enter()
        else:
            event.ignore()

    def mouse_enter_event(self, event):
        if self._active_handler is not None:
            self._active_handler.mouse_enter_event(event)

    def mouse_leave_event(self, event):
        if self._active_handler is not None:
            self._active_handler.mouse_leave_event(event)

    def mouse_press_event(self, event):
        """
        Handle a mouse press event in the scene viewer.
        """
        if self._active_handler is not None:
            self._active_handler.mouse_press_event(event)
        # self._use_zinc_mouse_event_handling = False  # Track when zinc should be handling mouse events
        # if self._ignore_mouse_events:
        #     event.ignore()
        #     return
        #
        # event.accept()
        # if event.button() not in button_map:
        #     return
        #
        # self._selection_position_start = (event.x(), event.y())
        #
        # if button_map[event.button()] == Sceneviewerinput.BUTTON_TYPE_LEFT \
        #         and self._selectionKeyPressed and (self._nodeSelectMode or self._elemSelectMode):
        #     self._selection_mode = SelectionMode.EXCLUSIVE
        #     if event.modifiers() & QtCore.Qt.SHIFT:
        #         self._selection_mode = SelectionMode.ADDITIVE
        # else:
        #     scene_input = self._sceneviewer.createSceneviewerinput()
        #     scene_input.setPosition(event.x(), event.y())
        #     scene_input.setEventType(Sceneviewerinput.EVENT_TYPE_BUTTON_PRESS)
        #     scene_input.setButtonType(button_map[event.button()])
        #     scene_input.setModifierFlags(modifier_map(event.modifiers()))
        #     self._sceneviewer.processSceneviewerinput(scene_input)
        #     self._use_zinc_mouse_event_handling = True

    def mouse_release_event(self, event):
        if self._active_handler is not None:
            self._active_handler.mouse_release_event(event)
        # if self._ignore_mouse_events:
        #     event.ignore()
        #     return
        # event.accept()
        #
        # if event.button() not in button_map:
        #     return
        #
        # if self._selection_mode != SelectionMode.NONE:
        #     self._removeSelectionBox()
        #     x = event.x()
        #     y = event.y()
        #     # Construct a small frustum to look for nodes in.
        #     scene = self._sceneviewer.getScene()
        #     region = scene.getRegion()
        #     region.beginHierarchicalChange()
        #
        #     scenepicker = self.getScenepicker()
        #     if (x != self._selection_position_start[0]) or (y != self._selection_position_start[1]):
        #         # box select
        #         left = min(x, self._selection_position_start[0])
        #         right = max(x, self._selection_position_start[0])
        #         bottom = min(y, self._selection_position_start[1])
        #         top = max(y, self._selection_position_start[1])
        #         scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT,
        #                                             left, bottom, right, top);
        #         if self._selection_mode == SelectionMode.EXCLUSIVE:
        #             self.clearSelection()
        #         if self._nodeSelectMode or self._dataSelectMode or self._elemSelectMode:
        #             selectionGroup = self.get_or_create_selection_group()
        #             if self._nodeSelectMode or self._dataSelectMode:
        #                 scenepicker.addPickedNodesToFieldGroup(selectionGroup)
        #             if self._elemSelectMode:
        #                 scenepicker.addPickedElementsToFieldGroup(selectionGroup)
        #
        #     else:
        #         # point select - get nearest object only
        #         scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT,
        #                                             x - self._selectTol, y - self._selectTol, x + self._selectTol,
        #                                             y + self._selectTol)
        #         nearestGraphics = scenepicker.getNearestGraphics()
        #         if (self._nodeSelectMode or self._dataSelectMode or self._elemSelectMode) \
        #                 and (self._selection_mode == SelectionMode.EXCLUSIVE) \
        #                 and not nearestGraphics.isValid():
        #             self.clearSelection()
        #
        #         if (self._nodeSelectMode and (nearestGraphics.getFieldDomainType() == Field.DOMAIN_TYPE_NODES)) or \
        #                 (self._dataSelectMode and (
        #                         nearestGraphics.getFieldDomainType() == Field.DOMAIN_TYPE_DATAPOINTS)):
        #             node = scenepicker.getNearestNode()
        #             if node.isValid():
        #                 nodeset = node.getNodeset()
        #                 selectionGroup = self.get_or_create_selection_group()
        #                 nodegroup = selectionGroup.getFieldNodeGroup(nodeset)
        #                 if not nodegroup.isValid():
        #                     nodegroup = selectionGroup.createFieldNodeGroup(nodeset)
        #                 group = nodegroup.getNodesetGroup()
        #                 if self._selection_mode == SelectionMode.EXCLUSIVE:
        #                     remove_current = (group.getSize() == 1) and group.containsNode(node)
        #                     selectionGroup.clear()
        #                     if not remove_current:
        #                         # re-find node group lost by above clear()
        #                         nodegroup = selectionGroup.getFieldNodeGroup(nodeset)
        #                         if not nodegroup.isValid():
        #                             nodegroup = selectionGroup.createFieldNodeGroup(nodeset)
        #                         group = nodegroup.getNodesetGroup()
        #                         group.addNode(node)
        #                 elif self._selection_mode == SelectionMode.ADDITIVE:
        #                     if group.containsNode(node):
        #                         group.removeNode(node)
        #                     else:
        #                         group.addNode(node)
        #
        #         if self._elemSelectMode and (nearestGraphics.getFieldDomainType() in \
        #                                      [Field.DOMAIN_TYPE_MESH1D, Field.DOMAIN_TYPE_MESH2D,
        #                                       Field.DOMAIN_TYPE_MESH3D, Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION]):
        #             elem = scenepicker.getNearestElement()
        #             if elem.isValid():
        #                 mesh = elem.getMesh()
        #                 selectionGroup = self.get_or_create_selection_group()
        #                 elementgroup = selectionGroup.getFieldElementGroup(mesh)
        #                 if not elementgroup.isValid():
        #                     elementgroup = selectionGroup.createFieldElementGroup(mesh)
        #                 group = elementgroup.getMeshGroup()
        #                 if self._selection_mode == SelectionMode.EXCLUSIVE:
        #                     remove_current = (group.getSize() == 1) and group.containsElement(elem)
        #                     selectionGroup.clear()
        #                     if not remove_current:
        #                         # re-find element group lost by above clear()
        #                         elementgroup = selectionGroup.getFieldElementGroup(mesh)
        #                         if not elementgroup.isValid():
        #                             elementgroup = selectionGroup.createFieldElementGroup(mesh)
        #                         group = elementgroup.getMeshGroup()
        #                         group.addElement(elem)
        #                 elif self._selection_mode == SelectionMode.ADDITIVE:
        #                     if group.containsElement(elem):
        #                         group.removeElement(elem)
        #                     else:
        #                         group.addElement(elem)
        #
        #     region.endHierarchicalChange()
        #     self._selection_mode = SelectionMode.NONE
        #
        # elif self._use_zinc_mouse_event_handling:
        #     scene_input = self._sceneviewer.createSceneviewerinput()
        #     scene_input.setPosition(event.x(), event.y())
        #     scene_input.setEventType(Sceneviewerinput.EVENT_TYPE_BUTTON_RELEASE)
        #     scene_input.setButtonType(button_map[event.button()])
        #     self._sceneviewer.processSceneviewerinput(scene_input)

    def mouse_move_event(self, event):
        if self._active_handler is not None:
            self._active_handler.mouse_move_event(event)
        # if self._ignore_mouse_events:
        #     event.ignore()
        #     return
        #
        # event.accept()
        #
        # if self._selection_mode != SelectionMode.NONE:
        #     x = event.x()
        #     y = event.y()
        #     xdiff = float(x - self._selection_position_start[0])
        #     ydiff = float(y - self._selection_position_start[1])
        #     if abs(xdiff) < 0.0001:
        #         xdiff = 1
        #     if abs(ydiff) < 0.0001:
        #         ydiff = 1
        #     xoff = float(self._selection_position_start[0]) / xdiff + 0.5
        #     yoff = float(self._selection_position_start[1]) / ydiff + 0.5
        #     self._addUpdateSelectionBox(xdiff, ydiff, xoff, yoff)
        #
        # elif self._use_zinc_mouse_event_handling:
        #     scene_input = self._sceneviewer.createSceneviewerinput()
        #     scene_input.setPosition(event.x(), event.y())
        #     scene_input.setEventType(Sceneviewerinput.EVENT_TYPE_MOTION_NOTIFY)
        #     if event.type() == QtCore.QEvent.Leave:
        #         scene_input.setPosition(-1, -1)
        #     self._sceneviewer.processSceneviewerinput(scene_input)

    def _addUpdateSelectionBox(self, xdiff, ydiff, xoff, yoff):
        # Using a non-ideal workaround for creating a rubber band for selection.
        # This will create strange visual artifacts when using two scene viewers looking at
        # the same scene.  Waiting on a proper solution in the API.
        # Note if the standard glyphs haven't been defined then the
        # selection box will not be visible
        scene = self._sceneviewer.getScene()
        scene.beginChange()
        if self._selectionBox is None:
            self._selectionBox = scene.createGraphicsPoints()
            self._selectionBox.setScenecoordinatesystem(SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT)
        attributes = self._selectionBox.getGraphicspointattributes()
        attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_CUBE_WIREFRAME)
        attributes.setBaseSize([xdiff, ydiff, 0.999])
        attributes.setGlyphOffset([xoff, -yoff, 0])
        # self._selectionBox.setVisibilityFlag(True)
        scene.endChange()

    def _removeSelectionBox(self):
        if self._selectionBox is not None:
            scene = self._selectionBox.getScene()
            scene.removeGraphics(self._selectionBox)
            self._selectionBox = None
