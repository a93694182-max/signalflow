import { NavLink } from 'react-router-dom'

function Header() {
  const getNavClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? 'header__nav-link active' : 'header__nav-link'

  return (
    <header className="header">
      <div>
        <NavLink className="header__brand" to="/">
          <span className="header__logo">SignalFlow</span>
          <span className="header__tagline">
            Follow the Flow. Discover the Why.
          </span>
        </NavLink>
      </div>

      <nav className="header__nav" aria-label="주요 메뉴">
        <NavLink
          to="/"
          className={getNavClass}
          end
        >
          Home
        </NavLink>

        <NavLink
          to="/timeline"
          className={getNavClass}
        >
          Timeline
        </NavLink>

        <NavLink
          to="/search"
          className={getNavClass}
        >
          Search
        </NavLink>

        <span className="header__status">
          Market Intelligence
        </span>
      </nav>
    </header>
  )
}

export default Header