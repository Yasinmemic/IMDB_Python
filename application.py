import requests
from bs4 import BeautifulSoup
from cefpython3 import cefpython as cef
import base64
import platform
import sys
import threading
import getFilmsInfo
from Film import Film
from Comment import Comment
sys.path.append("./Film/")

HTML_code = """
<!DOCTYPE html>
<html>

<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" /> 
    <style type="text/css">
        body,
        html {
            font-family: Arial;
            font-size: 11pt;
        }

        div.msg {
            margin: 0.2em;
            line-height: 1.4em;
        }

        b {
            background: #ccc;
            font-weight: bold;
            font-size: 10pt;
            padding: 0.1em 0.2em;
        }

        b.Python {
            background: #eee;
        }

        i {
            font-family: Courier new;
            font-size: 10pt;
            border: #eee 1px solid;
            padding: 0.1em 0.2em;
        }

        .card-title {
            font-size: 14px;
        } 
    </style>

</head>

<body>
    <div class="container">

     <div class="row mt-4">

                    <div class="col-md-4 offset-md-4 col-sm-4"><input type="text" placeholder="Search a Film" id="movieName" class="form-control"/></div>
                    <div class="col-md-4 col-sm-4">
                        <button type="button" class="btn btn-primary" onclick="searchFilm(document.getElementById('movieName').value)">Search</button>
                    </div>
                    <div class="col-md-12 mt-4 d-flex justify-content-center">
                        <h4>FILMLER</h4>
                    </div>
            </div>
     <div class="row mt-3" id="main">
     </div>

     <!-- Button trigger modal -->

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Film Comments</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body" id="modal_body">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
</div>



    <script>

    function js_print(lang, event, msg) {
        msg = "<b class="+lang+">"+lang+": "+event+":</b> " + msg;
        console = document.getElementById("console")
        console.innerHTML += "<div class=msg>"+msg+"</div>";
    }

    function js_callback_1(ret) {
        js_print("Javascript", "html_to_data_uri", ret);
    }

    function js_callback_2(msg, py_callback) {
        js_print("Javascript", "js_callback", msg);
        py_callback("String sent from Javascript");
    }

    window.onload = function(){
        js_print("Javascript", "window.onload", "Called");
        js_print("Javascript", "python_property", python_property);
        js_print("Javascript", "navigator.userAgent", navigator.userAgent);
        js_print("Javascript", "cefpython_version", cefpython_version.version);
        html_to_data_uri("test", js_callback_1);
        external.test_multiple_callbacks(js_callback_2);
    };
    </script>

    <script>

            function clear(){
                document.getElementById("main").innerHTML="";
                document.getElementById("yorumlar").innerHTML="";
                document.getElementById("foto").innerHTML="";
            }

            function displayFilms(name, link, id, image) {

                //row
                var row=document.createElement("div");
                //row.setAttribute("id", "Div1");
                row.setAttribute("data-id",id)
                row.className = "col-md-3 col-sm-3 mt-1";

                //card
                var card=document.createElement("div");
                card.className="card";
                card.style.width="18rem";

                //img
                var img=document.createElement("img");
                img.className="card-img-top";
                img.setAttribute('src', image);


                //card-body
                var card_body=document.createElement("div");
                card_body.className="card-body";
                var card_title=document.createElement("h5");
                card_title.className="card-title";
                card_title.innerHTML=name;
                var p=document.createElement("p");
                p.className="card-text";
                p.innerHTML="";

                var button=document.createElement("button");
                button.className="btn btn-primary";
                button.innerHTML="Yorumlar";
                button.setAttribute("data-toggle","modal");
                button.setAttribute("type","button");
                button.setAttribute("data-target","#exampleModal");
                button.setAttribute("data-link",link);
                button.setAttribute("data-name",name);
                button.setAttribute("data-image",image);
                button.setAttribute("data-id",id);

                card_body.appendChild(card_title);
                card_body.appendChild(p);
                card_body.appendChild(button);
                card.appendChild(img);
                card.appendChild(card_body);
                row.appendChild(card);
                var div=document.getElementById("main");
                div.appendChild(row);       
        }
        function displayComments(userName, comment){

            var user_icon=document.createElement("i");
            user_icon.className="fas fa-user";

            var comment_icon=document.createElement("i");
            comment_icon.className="fas fa-comment";

            var div_row=document.createElement("div");
            div_row.className="row";
            var div_username=document.createElement("div");
            div_username.className="col-md-12";
            div_username.append(user_icon);
            var b=document.createElement("b");
            b.innerHTML=userName +":";
            div_username.append(b);

            var div_comment_icon=document.createElement("div");
            div_comment_icon.className="col-md-2";

            div_comment_icon.append(comment_icon);
            var div_comment=document.createElement("div");
            div_comment.className="col-md-10";

            var p=document.createElement("p");
            p.innerHTML=comment;
            div_comment.append(p);
            var modal_body=document.getElementById("modal_body");   
            div_row.append(div_username);
            div_row.append(div_comment_icon);
            div_row.append(div_comment);
            modal_body.append(div_row);
            }


    </script>
    <script>

        $(function(){
            $('#exampleModal').on('show.bs.modal', function (event) {

                $("#modal_body").empty();

                var button=$(event.relatedTarget);
                var link=button.data("link");
                var name=button.data("name");
                var image=button.data("image");
                turkceAltyazi(link,name,image);
            })


            function batman(){
            alert("afsasf");
            }
        });
    </script>
</body>
</html>

"""
GetBrowser = ""


def main():

    check_versions()
    sys.excepthook = cef.ExceptHook
    settings = {
    }
    cef.Initialize(settings=settings)
    set_global_handler()
    global GetBrowser
    browser = cef.CreateBrowserSync(url=html_to_data_uri(HTML_code),
                                    window_title="Tutorial")

    GetBrowser = browser

    set_client_handlers(browser)
    set_javascript_bindings(browser)
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    ver = cef.GetVersion()
    print("[tutorial.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[tutorial.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[tutorial.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[tutorial.py] Python {ver} {arch}".format(
        ver=platform.python_version(),
        arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def html_to_data_uri(html, js_callback=None):

    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    if js_callback:
        js_print(js_callback.GetFrame().GetBrowser(),
                 "Python", "html_to_data_uri",
                 "Called from Javascript. Will call Javascript callback now.")
        js_callback.Call(ret)
    else:
        return ret


def set_global_handler():

    global_handler = GlobalHandler()
    cef.SetGlobalClientCallback("OnAfterCreated",
                                global_handler.OnAfterCreated)


def set_client_handlers(browser):
    client_handlers = [LoadHandler(), DisplayHandler()]
    for handler in client_handlers:
        browser.SetClientHandler(handler)


def set_javascript_bindings(browser):
    external = External(browser)
    bindings = cef.JavascriptBindings(
        bindToFrames=False, bindToPopups=False)

    bindings.SetProperty("python_property", "This property was set in Python")
    bindings.SetProperty("cefpython_version", cef.GetVersion())

    bindings.SetFunction("html_to_data_uri", html_to_data_uri)
    bindings.SetFunction("searchFilm", searchFilm)
    bindings.SetFunction("displayFilms", displayFilms)
    bindings.SetFunction("displayComments", displayComments)
    bindings.SetFunction("clear", clear)
    bindings.SetFunction("turkceAltyazi", turkceAltyazi)
    bindings.SetObject("external", external)
    browser.SetJavascriptBindings(bindings)


def turkceAltyazi(link, filmName, image):
    userNames = []
    comments = []
    Comments = []

    source = requests.get(
        'https://turkcealtyazi.org/yorumlar/'+link+filmName+".html")
    soup = BeautifulSoup(source.text, 'html.parser')

    userNames_source = soup.findAll(class_="ny3")
    for userName in userNames_source:
        userNames.append(userName.text)

    comment_source = soup.findAll(class_="ny8")
    for comment in comment_source:
        comments.append(comment.text)

    for co in range(len(comments)):
        comment = Comment(userNames[co], comments[co])
        Comments.append(comment)
        displayComments(GetBrowser, userNames[co], comments[co])


def displayComments(browser2, userName, comment):
    browser2.ExecuteFunction("displayComments", userName, comment)


def searchFilm(movieName):
    clear(GetBrowser)
    movieList = []
    movieList = getFilmsInfo.getFilms(movieName)

    for index in movieList:
        name = index.getName()
        link = index.getLink()
        image = index.getPhoto()
        id = index.getId()
        displayFilms(GetBrowser, name, id, link, image)


def displayFilms(browser, name, id, link, image):
    browser.ExecuteFunction("displayFilms", name, id, link, image)


def clear(browser):
    browser.ExecuteFunction("clear")


def js_print(browser, lang, event, msg):
    browser.ExecuteFunction("js_print", lang, event, msg)


class GlobalHandler(object):
    def OnAfterCreated(self, browser, **_):
        """Called after a new browser is created."""

        js_print(browser, "Python", "OnAfterCreated",
                 "This will probably never display as DOM is not yet loaded")

        args = [browser, "Python", "OnAfterCreated",
                "(Delayed) Browser id="+str(browser.GetIdentifier())]
        threading.Timer(0.5, js_print, args).start()


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:

            js_print(browser, "Python", "OnLoadingStateChange",
                     "Loading is complete")


class DisplayHandler(object):
    def OnConsoleMessage(self, browser, message, **_):
        """Called to display a console message."""

        if "error" in message.lower() or "uncaught" in message.lower():

            if "js_print is not defined" in message.lower():
                if hasattr(self, "js_print_is_not_defined"):
                    print("Python: OnConsoleMessage: "
                          "Intercepted Javascript error: "+message)
                    return
                else:
                    self.js_print_is_not_defined = True

            args = [browser, "Python", "OnConsoleMessage",
                    "(Delayed) Intercepted Javascript error: <i>{error}</i>"
                    .format(error=message)]
            threading.Timer(0.5, js_print, args).start()


class External(object):
    def __init__(self, browser):
        self.browser = browser

    def test_multiple_callbacks(self, js_callback):
        """Test both javascript and python callbacks."""
        js_print(self.browser, "Python", "test_multiple_callbacks",
                 "Called from Javascript. Will call Javascript callback now.")

        def py_callback(msg_from_js):
            js_print(self.browser, "Python", "py_callback", msg_from_js)
        js_callback.Call("String sent from Python", py_callback)


if __name__ == "__main__":
    main()
