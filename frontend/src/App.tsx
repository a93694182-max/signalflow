import './App.css'

import { BrowserRouter, Route, Routes } from 'react-router-dom'

import MainLayout from './layouts/MainLayout'
import FlowDetailPage from './pages/FlowDetailPage'
import HomePage from './pages/HomePage'
import SearchPage from './pages/SearchPage'
import TimelinePage from './pages/TimelinePage'

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/flows/:flowId"
            element={<FlowDetailPage />}
          />
          <Route path="/timeline" element={<TimelinePage />} />
          <Route path="/search" element={<SearchPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  )
}

export default App