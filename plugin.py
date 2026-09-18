@@
     def _dispatch_command(self, DeviceId, Unit, Command, Level, Hue, first_seen):
@@
         if Unit == 1:
             if Command in ("Off", "Close"):
                 commands["name"] = "close"
             elif Command in ("On", "Open"):
                 commands["name"] = "open"
@@
             else:
                 Domoticz.Error(f"Command {Command} not supported for unit 1")
                 return False
+        elif Unit == 4:
+            # Extra per-device discreet/slow roller shutter action.
+            if "Set Level" in Command:
+                commands["name"] = "setClosureAndLinearSpeed"
+                # Keep the shutter's normal "open = 0% / close = 100%" semantics
+                # while explicitly requesting the discreet/slow movement mode.
+                tmp = max(100 - int(Level), 0)
+                params.extend([tmp, "discreet"])
+                commands["parameters"] = params
+            elif Command in ("Off", "Close"):
+                commands["name"] = "setClosureAndLinearSpeed"
+                params.extend([0, "discreet"])
+                commands["parameters"] = params
+            elif Command in ("On", "Open"):
+                commands["name"] = "setClosureAndLinearSpeed"
+                params.extend([100, "discreet"])
+                commands["parameters"] = params
+            else:
+                Domoticz.Error(f"Command {Command} not supported for unit 4")
+                return False
         elif Unit == 2:
             if "Set Level" in Command:
                 commands["name"] = "setOrientation"
@@
             if device["definition"]["uiClass"] in ("VenetianBlind", "ExteriorVenetianBlind"):
                 Domoticz.Unit(Name=device["label"] + " up/down", Unit=1, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"], Used=used).Create()
                 Domoticz.Unit(Name=device["label"] + " orientation", Unit=2, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"], Used=used).Create()
+            elif device["definition"]["uiClass"] == "RollerShutter":
+                Domoticz.Unit(Name=device["label"], Unit=1, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"], Used=used).Create()
+                Domoticz.Unit(Name=device["label"] + " discreet", Unit=4, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"], Used=used).Create()
             else:
                 Domoticz.Unit(Name=device["label"], Unit=1, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"], Used=used).Create()
***