import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Badge } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

function App() {
  const [textEntries, setTextEntries] = useState([]);
  const [iconEntries, setIconEntries] = useState([]);
  const [barcodeEntries, setBarcodeEntries] = useState([]);
  const [previewBitmap, setPreviewBitmap] = useState(null);
  const [loading, setLoading] = useState(false);
  const [labelSettings, setLabelSettings] = useState({
    width: 100,
    height: 100,
    dpi: 300
  });

  // Component yüklendiğinde veritabanından verileri çek
  useEffect(() => {
    loadDataFromDatabase();
  }, []);

  const loadDataFromDatabase = async () => {
    try {
      // Text items'ları yükle
      const textResponse = await axios.get('/api/label/input-items');
      setTextEntries(textResponse.data);

      // Icon items'ları yükle
      const iconResponse = await axios.get('/api/label/icon-items');
      setIconEntries(iconResponse.data);

      // Barcode items'ları yükle
      const barcodeResponse = await axios.get('/api/label/barcode-items');
      setBarcodeEntries(barcodeResponse.data);

      // Label settings'leri yükle
      const settingsResponse = await axios.get('/api/label/label-settings');
      setLabelSettings(settingsResponse.data);

      toast.success('Veriler başarıyla yüklendi!');
    } catch (error) {
      console.error('Data loading error:', error);
      toast.error('Veriler yüklenirken hata oluştu!');
    }
  };

  // Text entries işlemleri
  const handleTextChange = (id, field, value) => {
    setTextEntries(prev => prev.map(entry => 
      entry.id === id ? { ...entry, [field]: value } : entry
    ));
  };

  const addTextEntry = () => {
    const newEntry = {
      id: Date.now(),
      text: 'Yeni Metin',
      x: 10,
      y: 10,
      fontSize: 12,
      fontFamily: 'Arial'
    };
    setTextEntries(prev => [...prev, newEntry]);
    toast.success('Yeni metin alanı eklendi!');
  };

  const removeTextEntry = (id) => {
    setTextEntries(prev => prev.filter(entry => entry.id !== id));
    toast.info('Metin alanı kaldırıldı!');
  };

  // Icon entries işlemleri
  const handleIconChange = (id, field, value) => {
    setIconEntries(prev => prev.map(entry => 
      entry.id === id ? { ...entry, [field]: value } : entry
    ));
  };

  const addIconEntry = () => {
    const newEntry = {
      id: Date.now(),
      x: 50,
      y: 50,
      width: 50,
      height: 50,
      base64String: ''
    };
    setIconEntries(prev => [...prev, newEntry]);
    toast.success('Yeni ikon alanı eklendi!');
  };

  const removeIconEntry = (id) => {
    setIconEntries(prev => prev.filter(entry => entry.id !== id));
    toast.info('İkon alanı kaldırıldı!');
  };

  const handleIconFileUpload = (id, file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target.result.split(',')[1];
      setIconEntries(prev => prev.map(entry => 
        entry.id === id ? { ...entry, base64String: base64 } : entry
      ));
    };
    reader.readAsDataURL(file);
  };

  // Barcode entries işlemleri
  const handleBarcodeChange = (id, field, value) => {
    setBarcodeEntries(prev => prev.map(entry => 
      entry.id === id ? { ...entry, [field]: value } : entry
    ));
  };

  const addBarcodeEntry = () => {
    const newEntry = {
      id: Date.now(),
      x: 50,
      y: 50,
      width: 50,
      height: 50,
      barcodeData: '1598524566',
      barcodeSequence: 1,
      barcodeFormat: 'CODE_39',
      textAlignment: 'left',
      textFontSize: 3,
      textFontFamily: 'Arial'
    };
    setBarcodeEntries(prev => [...prev, newEntry]);
    toast.success('Yeni barkod alanı eklendi!');
  };

  const removeBarcodeEntry = (id) => {
    setBarcodeEntries(prev => prev.filter(entry => entry.id !== id));
    toast.info('Barkod alanı kaldırıldı!');
  };

  const createBitmap = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/label/create-bitmap', {
        textEntries: textEntries,
        iconEntries: iconEntries,
        barcodeEntries: barcodeEntries
      });
      
      if (response.data.bitmap) {
        setPreviewBitmap(response.data.bitmap);
        toast.success('Bitmap başarıyla oluşturuldu!');
      }
    } catch (error) {
      console.error('Bitmap creation error:', error);
      toast.error('Bitmap oluşturulurken hata oluştu!');
    } finally {
      setLoading(false);
    }
  };

  const saveBitmapSettings = async () => {
    try {
      await axios.post('/api/label/save-settings', {
        textEntries: textEntries,
        iconEntries: iconEntries,
        barcodeEntries: barcodeEntries
      });
      toast.success('Bitmap ayarları kaydedildi!');
    } catch (error) {
      console.error('Save settings error:', error);
      toast.error('Ayarlar kaydedilirken hata oluştu!');
    }
  };

  const printLabels = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/label/print', {
        textEntries: textEntries,
        iconEntries: iconEntries,
        barcodeEntries: barcodeEntries
      });
      toast.success('Etiketler başarıyla yazdırıldı!');
    } catch (error) {
      console.error('Print error:', error);
      toast.error('Yazdırma işlemi başarısız!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Container fluid className="mt-3">
        {/* Header Buttons */}
        <Row className="mb-4">
          <Col className="d-flex justify-content-center gap-3">
            <Button 
              variant="primary" 
              size="lg"
              onClick={printLabels}
              disabled={loading}
            >
              Print Labels
            </Button>
            <Button 
              variant="primary" 
              size="lg"
              onClick={createBitmap}
              disabled={loading}
            >
              Bitmap Oluştur
            </Button>
            <Button 
              variant="outline-info" 
              size="lg"
              onClick={saveBitmapSettings}
              disabled={loading}
            >
              Bitmap Ayarlarını Kaydet
            </Button>
          </Col>
        </Row>

        <Row>
          {/* Sol Panel */}
          <Col md={6}>
            {/* Text Bilgileri */}
            <Card className="mb-4">
              <Card.Header className="bg-primary text-white">
                <h5 className="mb-0">Text Bilgileri</h5>
              </Card.Header>
              <Card.Body>
                {textEntries.map((entry, index) => (
                  <Card key={entry.id} className="mb-3 border-secondary">
                    <Card.Body>
                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Text:</strong></Form.Label>
                            <Form.Control
                              type="text"
                              value={entry.text}
                              onChange={(e) => handleTextChange(entry.id, 'text', e.target.value)}
                              placeholder="Metin girin"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>X:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.x}
                              onChange={(e) => handleTextChange(entry.id, 'x', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Y:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.y}
                              onChange={(e) => handleTextChange(entry.id, 'y', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Font Size:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.fontSize}
                              onChange={(e) => handleTextChange(entry.id, 'fontSize', parseInt(e.target.value) || 8)}
                              min="1"
                              max="72"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={6}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Font Family:</strong></Form.Label>
                            <Form.Select
                              value={entry.fontFamily}
                              onChange={(e) => handleTextChange(entry.id, 'fontFamily', e.target.value)}
                            >
                              <option value="Arial">Arial</option>
                              <option value="Arial Narrow">Arial Narrow</option>
                              <option value="Verdana">Verdana</option>
                              <option value="Times New Roman">Times New Roman</option>
                              <option value="Courier New">Courier New</option>
                              <option value="Tahoma">Tahoma</option>
                              <option value="Georgia">Georgia</option>
                              <option value="Comic Sans MS">Comic Sans MS</option>
                              <option value="Impact">Impact</option>
                              <option value="Lucida Console">Lucida Console</option>
                            </Form.Select>
                          </Form.Group>
                        </Col>
                      </Row>
                      <div className="d-flex justify-content-between align-items-center">
                        <Badge bg="info">Entry {index + 1}</Badge>
                        <Button 
                          variant="danger" 
                          size="sm"
                          onClick={() => removeTextEntry(entry.id)}
                        >
                          Sil
                        </Button>
                      </div>
                    </Card.Body>
                  </Card>
                ))}
                
                <Button 
                  variant="primary" 
                  onClick={addTextEntry}
                  className="w-100"
                >
                  Text Ekle
                </Button>
              </Card.Body>
            </Card>

            {/* İkon Bilgileri */}
            <Card className="mb-4">
              <Card.Header className="bg-success text-white">
                <h5 className="mb-0">İkon Bilgileri</h5>
              </Card.Header>
              <Card.Body>
                {iconEntries.map((entry, index) => (
                  <Card key={entry.id} className="mb-3 border-secondary">
                    <Card.Body>
                      <Row>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>X:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.x}
                              onChange={(e) => handleIconChange(entry.id, 'x', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Y:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.y}
                              onChange={(e) => handleIconChange(entry.id, 'y', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Width:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.width}
                              onChange={(e) => handleIconChange(entry.id, 'width', parseInt(e.target.value) || 10)}
                              min="10"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Height:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.height}
                              onChange={(e) => handleIconChange(entry.id, 'height', parseInt(e.target.value) || 10)}
                              min="10"
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Row>
                        <Col md={12}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>İcon:</strong></Form.Label>
                            <Form.Control
                              type="file"
                              accept="image/*"
                              onChange={(e) => handleIconFileUpload(entry.id, e.target.files[0])}
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <div className="d-flex justify-content-between align-items-center">
                        <Badge bg="success">İkon {index + 1}</Badge>
                        <Button 
                          variant="danger" 
                          size="sm"
                          onClick={() => removeIconEntry(entry.id)}
                        >
                          Sil
                        </Button>
                      </div>
                    </Card.Body>
                  </Card>
                ))}
                
                <Button 
                  variant="success" 
                  onClick={addIconEntry}
                  className="w-100"
                >
                  İkon Ekle
                </Button>
              </Card.Body>
            </Card>

            {/* Barkod Bilgileri */}
            <Card className="mb-4">
              <Card.Header className="bg-warning text-dark">
                <h5 className="mb-0">Barkod Bilgileri</h5>
              </Card.Header>
              <Card.Body>
                {barcodeEntries.map((entry, index) => (
                  <Card key={entry.id} className="mb-3 border-secondary">
                    <Card.Body>
                      <Row>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Sıra:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.barcodeSequence}
                              onChange={(e) => handleBarcodeChange(entry.id, 'barcodeSequence', parseInt(e.target.value) || 1)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>X:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.x}
                              onChange={(e) => handleBarcodeChange(entry.id, 'x', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Y:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.y}
                              onChange={(e) => handleBarcodeChange(entry.id, 'y', parseInt(e.target.value) || 0)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Width:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.width}
                              onChange={(e) => handleBarcodeChange(entry.id, 'width', parseInt(e.target.value) || 10)}
                              min="10"
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Row>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Height:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.height}
                              onChange={(e) => handleBarcodeChange(entry.id, 'height', parseInt(e.target.value) || 10)}
                              min="10"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Format:</strong></Form.Label>
                            <Form.Select
                              value={entry.barcodeFormat}
                              onChange={(e) => handleBarcodeChange(entry.id, 'barcodeFormat', e.target.value)}
                            >
                              <option value="CODE_128">CODE_128</option>
                              <option value="CODE_39">CODE_39</option>
                              <option value="QR_CODE">QR_CODE</option>
                            </Form.Select>
                          </Form.Group>
                        </Col>
                        <Col md={6}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Data:</strong></Form.Label>
                            <Form.Control
                              type="text"
                              value={entry.barcodeData}
                              onChange={(e) => handleBarcodeChange(entry.id, 'barcodeData', e.target.value)}
                              placeholder="Barkod verisi"
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Row>
                        <Col md={4}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Font Size:</strong></Form.Label>
                            <Form.Control
                              type="number"
                              value={entry.textFontSize}
                              onChange={(e) => handleBarcodeChange(entry.id, 'textFontSize', parseInt(e.target.value) || 3)}
                              min="1"
                              max="72"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={4}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Font Family:</strong></Form.Label>
                            <Form.Select
                              value={entry.textFontFamily}
                              onChange={(e) => handleBarcodeChange(entry.id, 'textFontFamily', e.target.value)}
                            >
                              <option value="Arial">Arial</option>
                              <option value="Arial Narrow">Arial Narrow</option>
                              <option value="Verdana">Verdana</option>
                              <option value="Times New Roman">Times New Roman</option>
                              <option value="Courier New">Courier New</option>
                              <option value="Tahoma">Tahoma</option>
                              <option value="Georgia">Georgia</option>
                              <option value="Comic Sans MS">Comic Sans MS</option>
                              <option value="Impact">Impact</option>
                              <option value="Lucida Console">Lucida Console</option>
                            </Form.Select>
                          </Form.Group>
                        </Col>
                        <Col md={4}>
                          <Form.Group className="mb-2">
                            <Form.Label><strong>Text Konum:</strong></Form.Label>
                            <Form.Select
                              value={entry.textAlignment}
                              onChange={(e) => handleBarcodeChange(entry.id, 'textAlignment', e.target.value)}
                            >
                              <option value="none">none</option>
                              <option value="center">center</option>
                              <option value="left">left</option>
                              <option value="right">right</option>
                            </Form.Select>
                          </Form.Group>
                        </Col>
                      </Row>
                      <div className="d-flex justify-content-between align-items-center">
                        <Badge bg="warning" text="dark">Barkod {index + 1}</Badge>
                        <Button 
                          variant="danger" 
                          size="sm"
                          onClick={() => removeBarcodeEntry(entry.id)}
                        >
                          Sil
                        </Button>
                      </div>
                    </Card.Body>
                  </Card>
                ))}
                
                <Button 
                  variant="warning" 
                  onClick={addBarcodeEntry}
                  className="w-100"
                >
                  Barkod Ekle
                </Button>
              </Card.Body>
            </Card>
          </Col>

          {/* Sağ Panel - Önizleme */}
          <Col md={6}>
            <Card>
              <Card.Header className="bg-secondary text-white">
                <h5 className="mb-0">Önizleme</h5>
              </Card.Header>
              <Card.Body>
                {previewBitmap ? (
                  <div className="text-center">
                    <img 
                      src={`data:image/bmp;base64,${previewBitmap}`} 
                      alt="Label Preview" 
                      className="img-fluid border"
                      style={{ maxWidth: '100%', maxHeight: '400px' }}
                    />
                    <p className="text-muted mt-2">Bitmap önizlemesi</p>
                  </div>
                ) : (
                  <div className="text-center py-5">
                    <p className="text-muted">
                      Henüz önizlenecek bitmap oluşturulmadı.
                    </p>
                    <Button 
                      variant="outline-primary" 
                      onClick={createBitmap}
                      disabled={loading}
                    >
                      Bitmap Oluştur
                    </Button>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
      
      <ToastContainer 
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App; 