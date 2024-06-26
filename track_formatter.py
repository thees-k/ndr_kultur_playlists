def format_track_info(track):
    (track_id, timestamp, title, movement, composer, full_title, image_link,
     catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir) = track

    title = format_field(title)
    movement = format_field(movement)
    composer = format_field(composer)
    catalog_number = format_field(catalog_number)
    conductor = format_field(conductor)
    orchestra = format_field(orchestra)
    solist = format_field(solist)
    album = format_field(album)
    ensemble = format_field(ensemble)
    ean = format_field(ean)
    choir = format_field(choir)

    perf = []
    if choir:
        perf.append(choir)
    if ensemble and ensemble not in perf:
        perf.append(ensemble)
    if orchestra and orchestra not in perf:
        perf.append(orchestra)

    composer_info = f"{composer}:" if composer else ""
    piece_and_movement = ", ".join(filter(None, [title, movement]))
    performers = ", ".join(filter(None, [solist, *perf, conductor]))
    performers = f"({performers})" if performers else ""
    album_info = "/".join(filter(None, [album, ean, catalog_number]))
    album_info = f"[{album_info}]" if album_info else ""
    track_info = " ".join(filter(None, [composer_info, piece_and_movement, performers, album_info]))

    return track_info


def format_field(field):
    return field.strip() if field and field.strip() != '-' and field.strip() != 'o. A.' else ""
