import axios from 'axios';
import express from 'express';

const app = express();
app.use(express.json());

app.get('/api/v1/search', async (req, res) => {
  const { type, keyword } = req.query;

  const { data } = await axios.get('https://myanimelist.net/search/prefix.json', {
    params: {
      type,
      keyword,
      v: 1,
    },
  });

  res.json(data);
});

const PORT = process.env['PORT'] || 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT} 🚀`));
