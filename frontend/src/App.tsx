import './App.css'

import { BrowserRouter, Route, Routes } from 'react-router-dom'

import MainLayout from './layouts/MainLayout'
import FlowDetailPage from './pages/FlowDetailPage'
import HomePage from './pages/HomePage'

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/flows/:flowId" element={<FlowDetailPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  )
}

export default App