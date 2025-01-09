# Properly cleans animal names by removing references and replacing slashes
# Generated with Qodo

# import pytest
from app.main import animals_and_adjectives_scrapping


def test_cleaning_animal_names(mocker):
    # Mock the requests.get response
    mock_response = mocker.Mock()
    mock_response.content = '''
        <table class="wikitable sortable sticky-header">
            <tr>
                <td><a href="/wiki/Ass/Donkey">Ass/Donkey[1]</a></td>
                <td>col2</td><td>col3</td><td>col4</td><td>col5</td>
                <td>asinine</td>
            </tr>
        </table>
    '''
    mocker.patch('requests.get', return_value=mock_response)

    # Mock the image scraping function
    mocker.patch('app.main.animals_and_images_scrapping', return_value={'Ass-Donkey': 'path/to/ass-donkey.jpg'})

    result = animals_and_adjectives_scrapping('https://example.com')

    assert 'Animals' in result
    assert 'Images' in result
    assert result['Animals'] == {'Ass-Donkey': ['asinine']}
    assert result['Images'] == {'Ass-Donkey': 'path/to/ass-donkey.jpg'}
