logFile="/usr/local/bin"
cd $logFile

#echo "$1"

# GET ---------------------------------------------------------

#查询区块链状态
if [ "$1" = "getinfo" ]; then
	hba=`/usr/local/bin/cleos -u $2 get info`;
	echo cleos -u $2 get info
	echo $hba
fi


#通过transaction_id获取交易
if [ "$1" = "gettransaction" ]; then
	hba=`/usr/local/bin/cleos -u $2 get transaction $3`;
	echo cleos -u $2 get transaction $3
	echo $hba
fi

#通过帐户获取交易
if [ "$1" = "gettransactionaccount" ]; then
	hba=`/usr/local/bin/cleos -u $2 get transaction $3`;
	echo cleos -u $2 get transaction $3
	echo $hba
fi


# 转账 ---------------------------------------------------------

#转账EOS cleos transfer ${from_account} ${to_account} ${quantity}
if [ "$1" = "transfer" ]; then
	hba=`/usr/local/bin/cleos -u $2 transfer $3 $4 $5`;
	echo cleos -u $2 transfer $3 $4 $5
	echo $hba
fi

# Wallet ---------------------------------------------------------

#创建钱包 cleos wallet create {-n} ${wallet_name}
if [ "$1" = "walletcreate" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet create -n $3`;
	echo cleos -u $2 wallet create -n $3
	echo $hba
fi

#钱包列表 cleos wallet list
if [ "$1" = "walletlist" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet list`;
	echo cleos -u $2 wallet list
	echo $hba
fi

#导入密钥 cleos wallet import ${key}
if [ "$1" = "walletimport" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet import $3`;
	echo cleos -u $2 wallet import $3
	echo $hba
fi

#key列表 cleos wallet keys
if [ "$1" = "walletkeys" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet keys`;
	echo cleos -u $2 wallet keys
	echo $hba
fi

#锁钱包 cleos wallet lock -n ${wallet_name}
if [ "$1" = "walletlock" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet lock -n $3`;
	echo cleos -u $2 wallet lock -n $3
	echo $hba
fi

#解锁钱包 cleos wallet unlock -n ${wallet_name} --password ${password}
if [ "$1" = "walletunlock" ]; then
	hba=`/usr/local/bin/cleos -u $2 wallet unlock -n $3 --password $4`;
	echo cleos -u $2 wallet unlock -n $3 --password $4
	echo $hba
fi

#打开钱包 cleos wallet open
if [ "$1" = "walletopen" ]; then
	hba=`/root/eos/build/programs/cleos/cleos -u $2 wallet open -n $3`;
	echo cleos -u $2 wallet open -n $3
	echo $hba
fi



# 帐户 ---------------------------------------------------------

#创建密钥	$ cleos create key
if [ "$1" = "createkey" ]; then
	hba=`/usr/local/bin/cleos -u $2 create key`;
	echo cleos -u $2 create key
	echo $hba
fi

#创建帐户	$ cleos create account ${control_account} ${account_name} ${owner_public_key} ${active_public_key}
if [ "$1" = "createaccount" ]; then
	hba=`/usr/local/bin/cleos -u $2 create account $3 $4 $5 $6`;
	echo cleos -u $2 create account $3 $4 $5 $6
	echo $hba
fi

#查看子账户	$ cleos get servants ${account_name}
if [ "$1" = "getservants" ]; then
	hba=`/usr/local/bin/cleos -u $2 get servants $3`;
	echo cleos -u $2 get servants $3
	echo $hba
fi

#检查帐户余额	$ cleos get account ${account_name}
if [ "$1" = "getaccount" ]; then
	hba=`/usr/local/bin/cleos -u $2 get account $3`;
	echo cleos -u $2 get account $3
	echo $hba
fi


# 权限 ---------------------------------------------------------

#创建或修改权限	$ cleos set account permission ${permission} ${account} ${permission_json} ${account_authority}
if [ "$1" = "setaccountpermission" ]; then
	hba=`/usr/local/bin/cleos -u $2 set account permission $3 $4 $5 $6`;
	echo cleos -u $2 get account $3
	echo $hba
fi


# 合约 ---------------------------------------------------------
#部署	$cleos set contract ../${contract}.wast ../${contract}.abi　or $cleos set contract ../${contract}	例子
if [ "$1" = "setcontract" ]; then
	hba=`/usr/local/bin/cleos -u $2 set contract $3 $4`;
	echo cleos -u $2 set contract $3 $4
	echo $hba
fi

#查询ABI	$ cleos get code -a ${contract}.abi ${contract}	例子
if [ "$1" = "getcode" ]; then
	hba=`/usr/local/bin/cleos -u $2 get code -a $3 $4`;
	echo cleos -u $2 get code -a $3 $4
	echo $hba
fi

#推送操作	$ cleos push action ${contract} ${action} ${param} -S ${scope_1} -S ${scope_2} -p ${account}@active	例子
if [ "$1" = "pushaction" ]; then
	hba=`/usr/local/bin/cleos -u $2 push action $3 $4 $5 -S $6 -S $7 -p $8@activ`;
	echo cleos -u $2 push action $3 $4 $5 -S $6 -S $7 -p $8@activ
	echo $hba
fi

#查询表	$ cleos get table ${field} ${contract} ${table}
if [ "$1" = "gettable" ]; then
	hba=`/usr/local/bin/cleos -u $2 get table  $3 $4 $5`;
	echo cleos -u $2 get table  $3 $4 $5
	echo $hba
fi


# RAM ---------------------------------------------------------

#购买
if [ "$1" = "buyram" ]; then
	hba=`/root/eos/build/programs/cleos/cleos -u $2 system buyram $3 $4 "$5 EOS";
	echo cleos -u $2 system buyram $3 $4 "$5 EOS"
	echo $hba
fi

#卖出
if [ "$1" = "sellram" ]; then
	hba=`/usr/local/bin/cleos -u $2 system sellram $3 $4;
	echo cleos -u $2 system sellram $3 $4
	echo $hba
fi