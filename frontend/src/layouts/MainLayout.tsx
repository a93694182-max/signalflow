import type { ReactNode } from 'react'

import Header from '../components/Header'

interface MainLayoutProps {
  children: ReactNode
}

function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="app">
      <Header />

      <div className="content">{children}</div>
    </div>
  )
}

export default MainLayout