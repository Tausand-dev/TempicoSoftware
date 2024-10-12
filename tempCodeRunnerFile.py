def indexChangeStartChannel(self):
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex()+1:
            self.comboBoxStartChannel.setCurrentIndex(self.oldStartChannelIndex)
        else:
            self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()