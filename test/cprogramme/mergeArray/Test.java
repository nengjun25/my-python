import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import jdk.javadoc.internal.doclets.formats.html.resources.standard;
import sun.tools.jconsole.MaximizableInternalFrame;

public class Test {
    public static void main(String[] args) {
        // mergeArray();
        phonestring();
    }

    static ArrayList<String> res = new ArrayList<>();

    private static void phonestring() {

        String num = "8763829";
        int l = num.length();

        ArrayList<String> collects = new ArrayList<>();

        for (int i = 0; i < l; i++) {
            switch (num.charAt(i)) {
                case 50:
                    collects.add("abc");
                    break;
                case 51:
                    collects.add("def");
                    break;
                case 52:
                    collects.add("ghi");
                    break;
                case 53:
                    collects.add("jkl");
                    break;
                case 54:
                    collects.add("mno");
                    break;
                case 55:
                    collects.add("pqrs");
                    break;
                case 56:
                    collects.add("tuv");
                    break;
                case 57:
                    collects.add("wxyz");
                    break;
                default:
                    break;
            }
        }

        System.out.println("run !" + collects.size() + "\n");
        backtrace(collects, new LinkedList<>(), 0);
        System.out.println("res size is " + res.size() + "\n");

    }

    private static void backtrace(List<String> collection, LinkedList<String> trace, int j) {
        if (trace.size() == collection.size()) {
            StringBuilder s = new StringBuilder();
            for (int i = 0; i < trace.size(); i++) {
                s.append(trace.get(i));
            }
            res.add(s.toString());
            return;
        }

        String choose = collection.get(j);

        for (int i = 0; i < choose.length(); i++) {

            String s = choose.substring(i, i + 1);
            trace.add(choose.substring(i, i + 1));
            j++;
            backtrace(collection, trace, j);
            trace.remove(choose.substring(i, i + 1));
            j--;
        }

    }

    private static void mergeArray() {
        int[][] section = { { 0, 1 }, { 2, 3 }, { 4, 7 }, { 6, 10 }, { 9, 11 } };
        int[][] after = new int[section.length][2];
        int j = 0;
        for (int i = 0; i < section.length; i++) {
            int[] merge = merge(after[j], section[i]);
            if (merge != null) {
                System.out.print("set after j = " + j + "\n");
                after[j] = merge;
                System.out.print("after j  is [ " + after[j][0] + "," + after[j][1] + "]\n");
            } else {
                j++;
                System.out.print("merge null after j = " + j + "\n");
                after[j] = section[i];
                System.out.print("merge null after j  is [ " + after[j][0] + "," + after[j][1] + "]\n");
            }
        }

        for (int k = 0; k <= j; k++) {
            System.out.print("section is [ " + after[k][0] + "," + after[k][1] + "]\n");
        }
    }

    private static int[] merge(int[] a, int[] b) {
        // todo
        if (a == null) {
            System.out.print("a null return b\n");
            return b;
        }

        if (b == null) {
            System.out.print("b null return a\n");
            return a;
        }

        if (a[1] >= b[0]) {
            int[] merge = new int[2];
            merge[0] = a[0];
            System.out.print("a1 is " + a[1] + "b0 is " + b[1] + "\n");
            if (a[1] <= b[1]) {
                merge[1] = b[1];
                System.out.print("merge is [ " + merge[0] + "," + merge[1] + "]\n");
                return merge;
            } else {
                System.out.print("return a\n");
                merge[1] = a[1];
                return merge;
            }
        }

        return null;

    }

}
