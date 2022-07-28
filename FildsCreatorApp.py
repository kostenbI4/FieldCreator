# import os
# os.environ['KIVY_IMAGE'] = 'pil'

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

import Main


class MyBox(Widget):
    inputText = ObjectProperty(None)
    finalText = ObjectProperty(None)
    chk_prime = ObjectProperty(None)
    chk_reports = ObjectProperty(None)

    def changeLabel(self):
        # print(self.finalText.text)
        print("chk_prime ", self.chk_prime.active)
        print("chk_reports ", self.chk_reports.active)
        if self.chk_prime.active:
            self.finalText.text = Main.getFilds(self.inputText.text)
        else:
            self.finalText.text = Main.getReportFilds(self.inputText.text)
        # self.label.text = Main.getFilds(self.textInput.text)


class FildsCreatorApp(App):

    def build(self):
        return MyBox()


if __name__ == "__main__":
    FildsCreatorApp().run()
