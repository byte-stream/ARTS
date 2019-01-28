# 常用排序算法

* 简单排序

    * 冒泡排序
    
        ```java
        public class BubbleSort {
        
            private static void method(int[] arr) {
                if(arr==null || arr.length==0) {
                    return ;
                }
                for(int x = 0; x < arr.length; x++) {
                    for(int y = 0; y < arr.length-1-x; y++) {
                        if(arr[y]>arr[y+1]) {
                            swap(arr, y, y+1);
                        }
                    }
                }
            }
        
            private static void swap(int[] arr, int m, int n) {
                int temp = arr[m];
                arr[m] = arr[n];
                arr[n] = temp;
            }
        }
        ```