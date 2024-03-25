RPC = "https://zetachain-evm.blockpi.network/v1/rpc/public"

# Значения
bnb_value_zeta = 0.00000036  # Сколько отдаем BNB в транзакции с пулом
pool_zeta_value = 0.0001  # Сколько отдаем ZETA в транзакции с пулом
bnb_to_approve = 0.0001  # Сколько аппрувить BNB в Zeta для транзакции с пулом (рекоммендуется аппрувнуть побольше для будущих транзакций с пулом - экономия газа)
zeta_value_btc = 0.001  # Сколько отдаем ZETA для транзакции ZETA->BTC.BTC (Выставленное самое минимальное значение)
zeta_value_eth = 0.0001  # Сколько отдаем ZETA для транзакции ZETA->ETH.ETH (Выставленное самое минимальное значение)
zeta_value_bnb = (
    0.001  # Сколько отдаем ZETA для транзакции ZETA->BNB.BSC (izumi finance)
)

eddy_finance_zeta = 2.3  # Сколько отдаем ZETA для свапа в BNB.BSC на EddyFinance (Следим за ценой ZETA т.к свап от $5)
acc_finance_zeta = 0.000001  # Сколько отдаем ZETA для транзакций на Accumulated Finance
range_protocol_zeta = 0.002  # Сколько отдаем ZETA для транзакций на Range Protocol.
zetaswap_zeta = 0.0001  # Сколько отдаем ZETA на квест Zetaswap (wZETA -> ETH.ETH)
badge_id = 21  # ID бейджа на Ultiverse
nativex_zeta = 0.001  # Сколько отдаем ZETA на квест Nativex Finance (ZETA -> BTC.BTC)

# Настройки времени
enroll_verify_time = 1.5  # Время между Enroll Verify
check_user_points_time = 1.5  # Время между проверкой XP|RANK|LEVEL
check_tasks_time = 0.5  # Время между проверкой выполненных квестов
claim_tasks_time = 3  # Время между клеймом выполненных квестов
transactions_break_time = 10  # Время между транзакциями
