# -*- coding:UTF-8 -*-

env = "PRE"
fab_ip = "http://private-api.nj.res.tuniu.org"
res_ip="http://public-api.nj.res.tuniu-sit.org"
fab_pebble_addr = "10.30.157.148:24993"
fab_pebble_version = "1.1.13"
zrb_ip = ""
zrb_pebble_addr = "10.30.157.148:24993"
zrb_pebble_version = "1.1.13"

#生产连不了数据库，配置没用
ttms_member=["tmc_member-master.db.tuniu-sit.org",3306,"tmc_member_rw","tuniu520","tmc_member"]
ttms_order=["tmc_order-master.db.tuniu-sit.org",3306,"tmc_order_rw","tuniu520","tmc_order"]

#单行程
single1 = {"product_id":"210034683","res_id":"1436032218","departs_date":"2018-05-03"}
single2 ={"product_id":"210034683","res_id":"1436032218","departs_date":"2018-05-03"}
#多行程
mult1 ={"product_id":"210034695","res_id":[2249900781],"departs_date":"2018-05-03"}
#可变行程
variable1 ={"product_id":"210034683","res_id":[2249900781,1436032218],"departs_date":"2018-05-03"}

apikey = "959c6671e34645adbd1244606dd2be6c"
secret="8897A384A5D2403BA125A798F9D2CBB7"
tmc_uid="15850552751"
# apikey = "dfdskl368jdsk563owe47839ky86"
# secret="655B0A326C872C21WEAF08C898WHT6C8"
# 商旅开放平台preprd域名
ttms_ops = "https://tmc.tuniu.com/ops"


TTMS_BSS="ttms-bss-api.tuniu-sit.com"
TTMS_CSS="ttms-css.api.tuniu-sit.org"
TTMS_DPTH="ttms-dpth.api.tuniu-sit.org"
TTMS_FINANCE="ttms-finance.api.tuniu-sit.org"
TTMS_GATEWAY="ttms-gateway.api.tuniu-sit.org"
TTMS_JOB="ttms-job.api.tuniu-sit.org"
TTMS_MEMBER="ttms-member.api.tuniu-sit.org"
TTMS_MSITE="public-api.msite.ttms.tuniu-sit.org"
TTMS_NBSS="ttms-nbss.api.tuniu-sit.org"
TTMS_NCSS="ttms-ncss.api.tuniu-sit.org"
TTMS_NMSITE="ttms-nmsite.api.tuniu-sit.org"
TTMS_ORDER="ttms-order.api.tuniu-sit.org"
TTMS_PRICE="ttms-price.api.tuniu-sit.org"
TTMS_SUPPLY="ttms-supply.api.tuniu-sit.org"
TTMS_SUPPORT="ttms-support.api.tuniu-sit.org"
TTMS_TRACE="ttms-trace.api.tuniu-sit.org"
