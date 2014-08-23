/*
 This utility is part of the clusterd attack framework.

 Used for encrypting/decrypting passwords for use in the Railo app server 
 */

public class RailoPasswordTool{

    public static void main(String args[]){
        if(args.length < 1)
        {
            System.out.println("Usage: java -cp . RailoPasswordTool e <password> to encrypt\njava -cp . RailoPasswordTool d <password> to decrypt");
            System.exit(1);
        }
        if(args[0].equals("d")){
            System.out.println(decrypt(args[1]));
        }
        else if(args[0].equals("e")){
            System.out.println(encrypt(args[1]));
        }
        else{
            System.out.println("Usage: java RailoPasswordTool e <password> to encrypt\njava RailoPasswordTool d <password> to decrypt");
        }
    }

    protected static String decrypt(String str) {
        return new BlowfishEasy("tpwisgh").decryptString(str);
    }
    protected static String encrypt(String str) {
        return new BlowfishEasy("tpwisgh").encryptString(str);
    }
}
