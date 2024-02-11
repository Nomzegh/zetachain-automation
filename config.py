RPC = "https://zetachain-mainnet-archive.allthatnode.com:8545"
BSC_RPC = "https://rpc.ankr.com/bsc"

# Значения
bnb_value_bsc = 0.000000001  # Сколько отправить BNB с BSC -> Zeta
bnb_value_zeta = 0.00000000000000001  # Сколько отдаем BNB в транзакции с пулом
pool_zeta_value = 0.000000000000001  # Сколько отдаем ZETA в транзакции с пулом
bnb_to_approve = 0.0001  # Сколько аппрувить BNB в Zeta для транзакции с пулом (рекоммендуется аппрувнуть побольше для будущих транзакций с пулом - экономия газа)
bsc_gasprice = 1.1  # gasPrice в BSC (не ставить ниже 1, так как транзакция зависнет)
zeta_value_btc = 0.001  # Сколько отдаем ZETA для транзакции ZETA->BTC.BTC (Выставленное самое минимальное значение)
zeta_value_eth = 0.0001  # Сколько отдаем ZETA для транзакции ZETA->ETH.ETH (Выставленное самое минимальное значение)
zeta_value_bnb = 0.001  # Сколько отдаем ZETA для транзакции ZETA->BNB.BSC (izumi finance)

# Настройки времени
enroll_verify_time = 1.5  # Время между Enroll Verify
check_user_points_time = 1.5  # Время между проверкой XP|RANK|LEVEL
check_tasks_time = 0.5  # Время между проверкой выполненных квестов
claim_tasks_time = 3  # Время между клеймом выполненных квестов
transactions_break_time = 2  # Время между транзакциями
