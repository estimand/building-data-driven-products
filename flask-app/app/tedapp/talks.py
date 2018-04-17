from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .db import get_similar_talks, query_talks


bp = Blueprint('talks', __name__)


@bp.route('/')
def index():
    talks = query_talks({
        'query': 'SELECT TOP 10 t.id, t.filmed_at, t.published_at, t.title ' \
                 'FROM talks t '
                 'ORDER BY t.published_at DESC',
    })
    return render_template('talks/index.html',
                           talks=talks)


@bp.route('/details/<id>', methods=('GET',))
def details(id):
    try:
        talk = next(x for x in query_talks({
            'query': 'SELECT TOP 1 * ' \
                     'FROM talks t ' \
                     'WHERE t.id = @id',
            'parameters': [
                {'name': '@id', 'value': id},
            ],
        }))
    except StopIteration:
        flash('Invalid talk', 'danger')
        return redirect(url_for('talks.index'))
    similar_talks = get_similar_talks(id)
    return render_template('talks/details.html',
                           talk=talk,
                           similar_talks=similar_talks)


@bp.route('/by-speaker/<id>', methods=('GET',))
def by_speaker(id):
    try:
        speaker = next(x for x in query_talks({
            'query': 'SELECT TOP 1 s.first_name, s.last_name, ' \
                     '             s.description, s.bio ' \
                     'FROM talks t ' \
                     'JOIN s IN t.speakers ' \
                     'WHERE s.id = @id',
            'parameters': [
                {'name': '@id', 'value': id},
            ],
        }))
    except StopIteration:
        flash('Invalid speaker', 'danger')
        return redirect(url_for('talks.index'))
    talks = query_talks({
        'query': 'SELECT t.id, t.filmed_at, t.title ' \
                 'FROM talks t ' \
                 'JOIN speaker IN t.speakers ' \
                 'WHERE speaker.id = @id '
                 'ORDER BY t.filmed_at DESC',
        'parameters': [
            {'name': '@id', 'value': id},
        ],
    })
    return render_template('talks/by-speaker.html',
                           speaker=speaker,
                           talks=talks)
