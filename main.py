from website import create_app, db
from website.models import Product

app = create_app()




if __name__ == '__main__':
    # unittest.main()
    app.run(debug=True)
