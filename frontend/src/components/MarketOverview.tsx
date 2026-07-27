import type { MarketItem } from '../types/market'

interface MarketOverviewProps {
  markets: MarketItem[]
}

function MarketOverview({ markets }: MarketOverviewProps) {
  return (
    <section>
      <div className="section-heading">
        <div>
          <p className="section-label">MARKET OVERVIEW</p>
          <h2>주요 시장 데이터</h2>
        </div>

        <span>{markets.length}개 자산</span>
      </div>

      {markets.length === 0 ? (
        <div className="empty-state">
          시장 데이터를 불러올 수 없습니다.
        </div>
      ) : (
        <div className="market-grid">
          {markets.map((market) => {
            const isUp = market.change > 0
            const isDown = market.change < 0

            const changeClassName = isUp
              ? 'market-card__change market-card__change--up'
              : isDown
                ? 'market-card__change market-card__change--down'
                : 'market-card__change'

            return (
              <article className="market-card" key={market.symbol}>
                <div className="market-card__top">
                  <span>{market.name}</span>
                  <small>{market.symbol}</small>
                </div>

                <strong className="market-card__price">
                  {market.price.toLocaleString('ko-KR', {
                    maximumFractionDigits: 2,
                  })}
                </strong>

                <div className={changeClassName}>
                  <span>
                    {market.change > 0 ? '+' : ''}
                    {market.change.toFixed(2)}
                  </span>

                  <span>
                    {market.change_percent > 0 ? '+' : ''}
                    {market.change_percent.toFixed(2)}%
                  </span>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </section>
  )
}

export default MarketOverview