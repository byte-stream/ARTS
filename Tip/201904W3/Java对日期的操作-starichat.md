# java 日期的各种操作
## 输出前一天，前一周，前一个月的时间
```
    // 格式化日期时间
	SimpleDateFormat  sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date dateNow = new Date();  //获取当前时间
		Calendar cl = Calendar.getInstance();  // 获取日历实例
		cl.setTime(dateNow);  //  当当前时间设置为日历实例的时间
//		cl.add(Calendar.DAY_OF_YEAR, -1);	//一天前的时间
//		cl.add(Calendar.WEEK_OF_YEAR, -1);	//一周前的时间
//		cl.add(Calendar.MONTH, -1);			//一月前的时间
		Date dateFrom = cl.getTime();

```
## 获取 UTC 时间，同时和本地时间转换
```
    public  class UTCTimeUtil {

    private static DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS") ;

    /**
     * 得到UTC时间，类型为字符串，格式为"yyyy-MM-dd HH:mm:ss.SSS" 例如：2019-04-13 10:03:10.125 (精确到毫秒级)
     * 如果获取失败，返回null
     * @return
     */
    public static String getUTCTime() {
        StringBuffer UTCTimeBuffer = new StringBuffer();
        // 取得本地时间日历实例
        Calendar cal = Calendar.getInstance() ;
        // 获取时间偏移量
        int zoneOffset = cal.get(java.util.Calendar.ZONE_OFFSET);
        // 获取夏令时差：
        int dstOffset = cal.get(java.util.Calendar.DST_OFFSET);
        // 从本地时间里扣除这些差量，即可以取得UTC时间：
        cal.add(java.util.Calendar.MILLISECOND, -(zoneOffset + dstOffset));
        int year = cal.get(Calendar.YEAR);
        int month = cal.get(Calendar.MONTH)+1;
        int day = cal.get(Calendar.DAY_OF_MONTH);
        int hour = cal.get(Calendar.HOUR_OF_DAY);
        int minute = cal.get(Calendar.MINUTE); 
        int second = cal.get(Calendar.SECOND);
        int milliSecond = cal.get(Calendar.MILLISECOND);
        UTCTimeBuffer.append(year).append("-").append(month).append("-").append(day) ;
        UTCTimeBuffer.append(" ").append(hour).append(":").append(minute).append(":").append(second).append(".").append(milliSecond) ;
        try{
            format.parse(UTCTimeBuffer.toString()) ;
            return UTCTimeBuffer.toString() ;
        }catch(ParseException e)
        {
            e.printStackTrace() ;
        }
        return null ;
    }

    /**
     * 将UTC时间转换为指定时区时间
     * @param UTCTime
     * @param timeZone  示例"GMT-8" 东八区
     * @return
     */
    public static String getLocalTimeFromUTC(String UTCTime,String timeZone){
        java.util.Date UTCDate = null ;
        String localTimeStr = null ;
        try {
            UTCDate = format.parse(UTCTime);
            format.setTimeZone(TimeZone.getTimeZone(timeZone)) ;
            localTimeStr = format.format(UTCDate) ;
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return localTimeStr ;
    }

    public static void main(String[] args) { 
        String UTCTimeStr = getUTCTimeStr() ;
        System.out.println(UTCTimeStr); 
        System.out.println(getLocalTimeFromUTC(UTCTimeStr,"GMT-8"));
    }

}
```