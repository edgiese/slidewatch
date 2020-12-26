Sub OnSlideShowPageChange()
    Dim slide_num As Integer
    slide_num = ActivePresentation.SlideShowWindow.View.CurrentShowPosition

    Dim Url As String, data As String
    Dim xml As Object

    Url = "http://127.0.0.1:5000/slide/" & slide_num
    Set xml = CreateObject("MSXML2.ServerXMLHTTP")
    With xml
        .Open "Get", Url, False
        .send
        data = .responseText
    End With

End Sub
