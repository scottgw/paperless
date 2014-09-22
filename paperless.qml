import QtQuick 1.0

Rectangle {
    // color: 'lightgray'

    ListView {
        id: documentListView

        anchors.fill: parent
        spacing: 5
        orientation: ListView.Horizontal
        height: parent.height

        model: documentModel

        delegate: Image {
            height: 200
            fillMode: Image.PreserveAspectFit
            smooth: true
            source: "image://document_images/" + modelData
        }

    }
}
