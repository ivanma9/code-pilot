app.get('/config.js', (req, res) => {
  res.set('Content-Type', 'application/javascript')
  res.send(`
    export const config = {
      GROQ_API_KEY: '${process.env.GROQ_API_KEY}'
    };
  `)
})
