# Vendredi-Noir
Gesture Interface + Multiplay Tetris

```bash
git clone https://github.com/wakame-tech/vendredi-noir.git
```

## Gesture UI

## TetrisClient
`W:10 x H:20`

[さんこう](http://zetcode.com/gui/pyqt5/tetris/)

![block](https://livedoor.blogimg.jp/mkomiz/imgs/f/f/ff82b30d.gif)

## TetrisServer
### skill stacks
- Python 3.7.5
- Flask
- Flask-SocketIO

### API schema
schema from server

```json
{
  "score": "120",
  "falling": {
    "type": "O",
    "pos": [3, 5]
  },
  "next": "J",
  "board": [
    [0, 0, 0, ...],
    [0, 0, 0, ...],
    ...
    [0, 1, 2, ...],
  ],
  "isDead": false
}
```

### deploy to heroku
```
git subtree push --prefix src/server/ heroku master
```

deployed at [here](https://vendredi-noir.herokuapp.com) 🎉🎉🎉


### ref
- <https://devcenter.heroku.com/articles/python-websockets>
- <https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py>
