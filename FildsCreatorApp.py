import os
os.environ['KIVY_IMAGE'] = 'pil'

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

import Main


class MyBox(Widget):
    inputText = ObjectProperty(None)
    finalText = ObjectProperty(None)

    def changeLabel(self):
        print(self.finalText.text)
        self.finalText.text = Main.getFilds(self.inputText.text)
        # self.label.text = Main.getFilds(self.textInput.text)


class FildsCreatorApp(App):

    def build(self):
        return MyBox()


if __name__ == "__main__":
    FildsCreatorApp().run()
