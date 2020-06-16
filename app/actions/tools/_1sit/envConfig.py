# -*- coding:UTF-8 -*-

env = "SIT"
fab_ip = "http://private-api.nj.res.tuniu.org"
res_ip="http://public-api.nj.res.tuniu-sit.org"
fab_pebble_addr = "10.30.157.148:24993"
fab_pebble_version = "1.1.13"
zrb_ip = ""
zrb_pebble_addr = "10.30.157.148:24993"
zrb_pebble_version = "1.1.13"
pur_ip = "http://public-api.nj.pur.tuniu-sit.org"
stk_ip = "http://public-api.nj.stk.tuniu-sit.org"
prd_ip = "http://public-api.pms.mcs.tuniu-sit.org"

pur_db_ip="pur_nm-master.db.tuniu-sit.org"
pur_db_port=3306
pur_db_user="pur_nm_rw"
pur_db_pwd="tuniu520"
pur_db_space="pur_nm"
pur_db_info=["pur_nm-master.db.tuniu-sit.org",3306,"pur_nm_rw","tuniu520","pur_nm"]

stk_db_ip="stk_nm-master.db.tuniu-sit.org"
stk_db_port=3306
stk_db_user="stk_nm_rw"
stk_db_pwd="tuniu520"
stk_db_space="stk_nm"
stk_db_info=["stk_nm-master.db.tuniu-sit.org",3306,"stk_nm_rw","tuniu520","stk_nm"]

res_db_info=["res_nm-master.db.tuniu-sit.org",3306,"res_nm_rw","tuniu520","res_nm"]
prd_db_info=["prd_nm-master.db.tuniu-sit.org",3306,"prd_nm_rw","tuniu520","prd_nm"]

ttms_member=["tmc_member-master.db.tuniu-sit.org",3306,"tmc_member_rw","tuniu520","tmc_member"]
ttms_order=["tmc_order-master.db.tuniu-sit.org",3306,"tmc_order_rw","tuniu520","tmc_order"]

pjbres_db_info=["hx-jpt_res-jpt_res-master.db.tuniu-sit.org",3306,"jpt_res_rw","tuniu520","jpt_res"]
pjbprd_db_info=["hx-jpt_prd-jpt_prd-master.db.tuniu-sit.org",3306,"jpt_prd_rw","tuniu520","jpt_prd"]


jptord_db_info=["hx-jpt_ord-jpt_ord-master.db.tuniu-sit.org",3306,"jpt_ord_rw","tuniu520","jpt_ord"]
jptstk_db_info=["hx-jpt_stk-jpt_stk-master.db.tuniu-sit.org",3306,"jpt_stk_rw","tuniu520","jpt_stk"]

agreementAttachment=[
    {
      "fileName": "aa.pdf",
      "filePath": "http://10.10.32.160/fb2/t1/group1/M00/00/4E/CgogolsON-yIEJ4hAADOBHqLjMkAAAD0gPKyGYAAM4c582.pdf"
    }
  ]

payCompanyId="12"



#单行程
single1 = {"product_id":"210034683","res_id":"1436032218","departs_date":"2018-05-03"}
single2 ={"product_id":"210034683","res_id":"1436032218","departs_date":"2018-05-03"}
#多行程
mult1 ={"product_id":"210034695","res_id":[2249900781],"departs_date":"2018-05-03"}
#可变行程
variable1 ={"product_id":"210034683","res_id":[2249900781,1436032218],"departs_date":"2018-05-03"}


channelRelationself={"channelRelationId":"010000000000","pricing_type":"1"}
channelRelationother={"channelRelationId":"020110000000","pricing_type":"2"}

# apikey="dfdsklakfjdskffiowe478392l28"
# secret=None
# tmc_uid="18911112146"
apikey="dfdsklakfjdskffiowe478392l45"
secret=None
tmc_uid="18062527068"
# 商旅开放平台sit域名
ttms_ops = "https://ttms-ops-api.tuniu-sit.com"
ttms_adapter="https://ttms-adapter-api.tuniu-sit.com/adapter/ccb"
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
