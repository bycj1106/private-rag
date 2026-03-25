import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import UploadPage from './pages/UploadPage'
import DocumentsPage from './pages/DocumentsPage'
import QueryPage from './pages/QueryPage'
import DocumentDetailPage from './pages/DocumentDetailPage'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/documents/:id" element={<DocumentDetailPage />} />
          <Route path="/query" element={<QueryPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
